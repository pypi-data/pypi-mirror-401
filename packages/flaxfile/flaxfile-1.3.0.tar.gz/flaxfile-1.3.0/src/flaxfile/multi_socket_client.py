#!/usr/bin/env python3
"""
FlaxFile 真正的多Socket客户端

架构：N个独立socket，每个socket使用滑动窗口
总并发 = N × window_size

服务器端支持：
- 多个identity可以协同上传同一个file_key
- 按file_key而不是identity管理上传会话
"""

import asyncio
import time
import hashlib
import json
import aiofiles
from pathlib import Path
from typing import Dict, Any, List, Optional

import zmq
import zmq.asyncio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn, DownloadColumn

from .crypto import get_password, configure_client_encryption, derive_server_keypair
from loguru import logger

console = Console()


class MultiSocketFlaxFileClient:
    """真正的多Socket + 滑动窗口客户端"""

    # 类级别的公钥缓存（按密码哈希缓存，避免重复 PBKDF2 计算）
    _server_public_key_cache: dict = {}

    def __init__(
        self,
        server_host: str = "127.0.0.1",
        port: int = 25555,
        password: Optional[str] = None,
        num_connections: Optional[int] = None,
        window_size: int = 8,
        silent: bool = False,
        shared_context: Optional[zmq.asyncio.Context] = None
    ):
        self.server_host = server_host
        self.port = port
        self.password = password
        self.num_connections = num_connections
        self.window_size = window_size
        self.silent = silent  # 静默模式，不打印连接信息

        # 支持共享 context（避免创建过多 context 导致资源耗尽）
        self.context = shared_context if shared_context else zmq.asyncio.Context()
        self._owns_context = shared_context is None  # 记录是否拥有 context
        self.sockets = []
        self.connected = False

        # 🔥 优化：预计算服务器公钥（使用类级别缓存，避免 sync.py 中多文件重复计算）
        # 对于批量上传（32个文件 x 16个socket），可以节省约45秒的PBKDF2计算时间
        self.server_public_key = None
        if password:
            # 使用密码作为缓存键（安全：密码本身不持久化，只缓存派生的公钥）
            cache_key = password
            if cache_key not in MultiSocketFlaxFileClient._server_public_key_cache:
                _, public_key = derive_server_keypair(password)
                MultiSocketFlaxFileClient._server_public_key_cache[cache_key] = public_key
            self.server_public_key = MultiSocketFlaxFileClient._server_public_key_cache[cache_key]

    def _get_optimal_chunk_size(self, file_size: int) -> int:
        """
        根据文件大小和网络类型确定最优chunk size（KISS优化）
        远程传输使用更大的chunk减少往返次数
        """
        # 检测是否为本地传输
        is_local = self.server_host in ['127.0.0.1', 'localhost', '::1']

        if is_local:
            # 本地传输：保持4MB chunk
            return 4 * 1024 * 1024
        else:
            # 远程传输：使用更大的chunk减少往返次数
            if file_size < 50 * 1024 * 1024:  # < 50MB
                return 8 * 1024 * 1024   # 8MB
            elif file_size < 500 * 1024 * 1024:  # < 500MB
                return 16 * 1024 * 1024  # 16MB
            else:  # >= 500MB
                return 32 * 1024 * 1024  # 32MB

    def _auto_determine_config(self, file_size: int) -> tuple:
        """自动确定最优配置"""
        if self.num_connections:
            # 如果用户指定了连接数，窗口大小根据是否远程调整
            is_remote = self.server_host not in ['127.0.0.1', 'localhost', '::1']
            window = 32 if is_remote else self.window_size
            return self.num_connections, window

        # 检测是否为远程传输
        is_remote = self.server_host not in ['127.0.0.1', 'localhost', '::1']

        # 自适应策略: 文件边界为 1MB, 10MB, 100MB, 1GB
        # 每文件socket数: 1, 4, 8, 16
        # 远程传输使用更大的窗口（32）来应对高RTT
        if file_size < 1 * 1024 * 1024:  # <1MB
            return 1, 32 if is_remote else 16
        elif file_size < 10 * 1024 * 1024:  # <10MB
            return 4, 32 if is_remote else 8
        elif file_size < 100 * 1024 * 1024:  # <100MB
            return 8, 32 if is_remote else 8
        elif file_size < 1024 * 1024 * 1024:  # <1GB
            return 16, 32 if is_remote else 8
        else:  # >=1GB
            return 16, 32 if is_remote else 8

    async def connect(self, num_connections: int):
        """创建多个socket连接（并行建立）"""
        # 如果已有足够的socket，直接返回
        if self.connected and len(self.sockets) >= num_connections:
            return

        # 如果需要更多socket，创建额外的
        if not self.connected:
            self.sockets = []
            start_idx = 0
        else:
            start_idx = len(self.sockets)

        # 🔥 KISS优化：并行创建所有Socket，避免串行等待
        async def create_and_test_socket(idx: int):
            """创建并测试单个socket连接"""
            sock = self.context.socket(zmq.DEALER)
            sock.setsockopt(zmq.SNDBUF, 128 * 1024 * 1024)
            sock.setsockopt(zmq.RCVBUF, 128 * 1024 * 1024)
            sock.setsockopt(zmq.LINGER, 0)

            # 使用预计算的服务器公钥
            encryption_enabled = configure_client_encryption(
                sock,
                self.password,
                server_public_key=self.server_public_key
            )
            sock.connect(f"tcp://{self.server_host}:{self.port}")

            # 测试连接（带超时，防止无限等待）
            try:
                await sock.send_multipart([b'', b'PING'])
                frames = await asyncio.wait_for(sock.recv_multipart(), timeout=5.0)
                if len(frames) < 2 or frames[1] != b'PONG':
                    raise ConnectionError(f"Socket {idx} 连接失败: 无效响应")
            except asyncio.TimeoutError:
                sock.close()
                raise ConnectionError(f"Socket {idx} 连接超时（5秒）")

            return sock, encryption_enabled

        # 并行创建所有Socket
        tasks = [create_and_test_socket(i) for i in range(start_idx, num_connections)]
        results = await asyncio.gather(*tasks)

        # 添加到socket列表
        encryption_enabled = None
        for sock, enc in results:
            self.sockets.append(sock)
            encryption_enabled = enc  # 记录最后一个的加密状态（都相同）

        # 移除加密连接提示：这个信息对用户来说是技术细节，不需要在终端显示
        # 如果需要调试连接状态，应该使用日志系统而不是直接打印到终端

        self.connected = True

    async def upload_file(
        self,
        file_path: str,
        file_key: str,
        chunk_size: int = 4 * 1024 * 1024,
        show_progress: bool = False,
        session_id: str = None,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """
        真正的多Socket并发上传

        架构：
        - Socket 0: chunks [0, N, 2N, 3N, ...]
        - Socket 1: chunks [1, N+1, 2N+1, ...]
        - ...
        每个socket内部使用滑动窗口

        Args:
            session_id: 会话ID（用于支持多文件并发上传），如果不提供则自动生成UUID
            progress_callback: 进度回调函数，接收参数 (bytes_uploaded: int, total_bytes: int)
        """
        import uuid

        # 🔥 详细耗时统计
        overall_start = time.time()

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        file_size = file_path.stat().st_size

        # 自动选择最优chunk size（KISS优化 - 减少远程传输往返次数）
        if chunk_size is None or chunk_size == 4 * 1024 * 1024:
            chunk_size = self._get_optimal_chunk_size(file_size)

        total_chunks = (file_size + chunk_size - 1) // chunk_size

        # 生成或使用提供的session_id
        if session_id is None:
            session_id = str(uuid.uuid4())

        # 自动确定配置
        num_sockets, window_size = self._auto_determine_config(file_size)

        # 创建连接
        connect_start = time.time()
        await self.connect(num_sockets)
        connect_time = time.time() - connect_start

        # 实际传输开始
        transfer_start = time.time()

        # 全局进度跟踪 - 使用字典无锁方案（KISS优化）
        bytes_uploaded_per_socket = {}  # 每个socket维护自己的进度，避免锁竞争
        upload_done = asyncio.Event()  # 添加完成标志
        all_ready = asyncio.Event()  # 所有socket准备就绪的信号

        # 单个socket的工作线程
        async def socket_worker(socket_idx: int):
            """每个socket负责: socket_idx, socket_idx+N, socket_idx+2N, ..."""
            bytes_uploaded_per_socket[socket_idx] = 0  # 初始化本socket的进度

            socket = self.sockets[socket_idx]
            my_chunks = list(range(socket_idx, total_chunks, num_sockets))

            if not my_chunks:
                return 0

            # 每个socket独立注册上传会话（发送session_id）
            await socket.send_multipart([
                b'', b'UPLOAD_START_CONCURRENT',
                session_id.encode('utf-8'),  # 新增：session_id
                file_key.encode('utf-8'),
                str(file_size).encode('utf-8'),
                str(window_size).encode('utf-8')
            ])
            frames = await socket.recv_multipart()
            if len(frames) < 2 or frames[1] != b'OK':
                error_msg = frames[2].decode('utf-8') if len(frames) > 2 else "Unknown error"
                raise Exception(f"Socket {socket_idx} 上传准备失败: {error_msg}")

            # 等待所有socket都准备好
            await all_ready.wait()

            # 滑动窗口状态
            pending_acks = {}
            bytes_sent = 0
            window_available = asyncio.Event()  # 窗口可用事件
            window_available.set()  # 初始窗口有空间
            last_callback_time = 0  # 上次进度回调的时间（节流用）

            # 发送者
            async def sender():
                nonlocal bytes_sent

                async with aiofiles.open(file_path, 'rb') as f:
                    for chunk_id in my_chunks:
                        # 等待窗口有空间（事件驱动，避免忙轮询）
                        while len(pending_acks) >= window_size:
                            window_available.clear()
                            await window_available.wait()

                        # 读取chunk
                        offset = chunk_id * chunk_size
                        await f.seek(offset)
                        chunk_data = await f.read(chunk_size)

                        if not chunk_data:
                            break

                        # 发送
                        await socket.send_multipart([
                            b'', b'UPLOAD_CHUNK_CONCURRENT',
                            str(chunk_id).encode('utf-8'),
                            chunk_data
                        ])

                        pending_acks[chunk_id] = (time.time(), len(chunk_data))

            # 接收者
            async def receiver():
                nonlocal bytes_sent

                acks_received = 0
                while acks_received < len(my_chunks):
                    frames = await socket.recv_multipart()
                    if len(frames) < 3 or frames[1] != b'ACK':
                        logger.warning(f"Socket {socket_idx} 收到非ACK: {frames}")
                        # 收到非ACK消息，可能是服务器的其他响应，继续等待下一条
                        continue

                    ack_chunk_id = int(frames[2].decode('utf-8'))

                    if ack_chunk_id in pending_acks:
                        _, chunk_len = pending_acks.pop(ack_chunk_id)
                        bytes_sent += chunk_len
                        acks_received += 1
                        window_available.set()  # 通知 sender 窗口有空间

                        # 更新本socket的进度（无锁，KISS优化）
                        bytes_uploaded_per_socket[socket_idx] = bytes_sent
                        # 进度回调节流：避免频繁调用（每 100ms 更新一次）
                        if progress_callback:
                            nonlocal last_callback_time
                            current_time = time.time()
                            if current_time - last_callback_time >= 0.1:  # 100ms 节流
                                last_callback_time = current_time
                                try:
                                    total_uploaded = sum(bytes_uploaded_per_socket.values())
                                    if asyncio.iscoroutinefunction(progress_callback):
                                        await progress_callback(total_uploaded, file_size)
                                    else:
                                        progress_callback(total_uploaded, file_size)
                                except Exception as e:
                                    logger.warning(f"进度回调失败: {e}")

            # 并发运行
            await asyncio.gather(sender(), receiver())

            # 结束上传
            await socket.send_multipart([b'', b'UPLOAD_END'])
            frames = await socket.recv_multipart()

            return bytes_sent

        # 并发运行所有socket
        if show_progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                upload_task = progress.add_task(
                    f"[cyan]上传中",
                    total=file_size
                )

                # 进度更新协程
                async def progress_updater():
                    last_bytes = 0
                    while not upload_done.is_set():
                        await asyncio.sleep(0.1)
                        current_bytes = sum(bytes_uploaded_per_socket.values())
                        if current_bytes > last_bytes:
                            progress.update(upload_task, completed=current_bytes)
                            last_bytes = current_bytes
                    # 最后一次更新
                    final_bytes = sum(bytes_uploaded_per_socket.values())
                    progress.update(upload_task, completed=final_bytes)

                # 启动进度更新
                progress_task = asyncio.create_task(progress_updater())

                # 启动所有worker（它们会在UPLOAD_START完成后等待all_ready信号）
                tasks = [asyncio.create_task(socket_worker(i)) for i in range(num_sockets)]

                # 等待所有worker完成UPLOAD_START注册
                await asyncio.sleep(0.1)

                # 发送all_ready信号，让所有worker开始发送chunk
                all_ready.set()

                # 等待所有worker完成
                results = await asyncio.gather(*tasks)
                bytes_total = sum(results)

                # 通知进度更新完成
                upload_done.set()
                await progress_task
        else:
            # 启动所有worker
            tasks = [asyncio.create_task(socket_worker(i)) for i in range(num_sockets)]

            # 等待所有worker完成UPLOAD_START注册
            await asyncio.sleep(0.1)

            # 发送all_ready信号
            all_ready.set()

            # 等待所有worker完成
            results = await asyncio.gather(*tasks)
            bytes_total = sum(results)

        # 计算详细耗时
        transfer_time = time.time() - transfer_start
        total_time = time.time() - overall_start
        prepare_time = connect_time  # 准备时间主要是连接建立

        throughput = (file_size / (1024 * 1024)) / transfer_time if transfer_time > 0 else 0

        if show_progress:
            from rich.table import Table
            # 4列布局（2对键值），更紧凑
            table = Table(title="[bold green]✓ 上传完成", show_header=False, border_style="green", show_edge=False, padding=(0, 1))
            table.add_column(style="dim", justify="right")
            table.add_column(style="")
            table.add_column(style="dim", justify="right")
            table.add_column(style="")

            table.add_row("文件", f"[cyan]{file_key}[/cyan]", "大小", f"[yellow]{file_size / (1024*1024):.2f} MB[/yellow]")
            table.add_row("总耗时", f"[magenta]{total_time:.2f}秒[/magenta]", "吞吐量", f"[green]{throughput:.2f} MB/s[/green]")
            console.print(table)

        return {
            'file_key': file_key,
            'size': file_size,
            'transfer_time': transfer_time,
            'prepare_time': prepare_time,
            'total_time': total_time,
            'throughput': throughput,
            'num_sockets': num_sockets,
            'window_size': window_size,
            'total_concurrency': num_sockets * window_size
        }

    async def download_file(
        self,
        file_key: str,
        output_path: str,
        chunk_size: int = 4 * 1024 * 1024,
        show_progress: bool = False,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """多Socket并发下载（与现有实现类似）"""
        # 🔥 详细耗时统计
        overall_start = time.time()

        # 先获取文件信息
        if not self.connected or not self.sockets:
            await self.connect(1)

        # 🔥 KISS优化：向服务器传递期望的chunk_size，减少chunk数量
        # 服务器会根据客户端请求使用相应的chunk_size
        await self.sockets[0].send_multipart([
            b'', b'DOWNLOAD_START_CONCURRENT',
            file_key.encode('utf-8'),
            str(chunk_size).encode('utf-8')  # 传递期望的chunk_size
        ])

        frames = await self.sockets[0].recv_multipart()

        # 检查响应
        if len(frames) < 2:
            raise Exception(f"服务器响应格式错误")

        if frames[1] == b'ERROR':
            error_msg = frames[2].decode('utf-8') if len(frames) > 2 else "Unknown error"
            raise FileNotFoundError(f"下载失败: {error_msg}")

        if frames[1] != b'OK' or len(frames) < 5:
            raise FileNotFoundError(f"文件不存在: {file_key}")

        file_size = int(frames[2].decode('utf-8'))
        total_chunks = int(frames[3].decode('utf-8'))
        server_chunk_size = int(frames[4].decode('utf-8'))

        # 使用服务器返回的chunk_size（服务器可能调整了客户端请求的值）
        chunk_size = server_chunk_size

        # 自动确定配置
        num_sockets, window_size = self._auto_determine_config(file_size)

        # 创建更多连接
        connect_start = time.time()
        if len(self.sockets) < num_sockets:
            await self.connect(num_sockets)
        connect_time = time.time() - connect_start

        # 实际传输开始
        transfer_start = time.time()

        # 用于按序写入的buffer
        chunks_buffer = {}
        next_write_id = 0
        bytes_received = 0
        buffer_lock = asyncio.Lock()
        hash_obj = hashlib.sha256()
        download_done = asyncio.Event()  # 添加完成标志
        chunk_ready = asyncio.Event()  # 有新chunk可写入的事件
        buffer_space_available = asyncio.Event()  # 缓冲区有空间的事件
        buffer_space_available.set()  # 初始缓冲区有空间
        # 限制缓冲区大小，避免内存无限增长（背压机制）
        max_buffer_chunks = window_size * num_sockets * 2

        # 单个socket的下载线程
        async def socket_worker(socket_idx: int):
            socket = self.sockets[socket_idx]
            my_chunks = list(range(socket_idx, total_chunks, num_sockets))

            if not my_chunks:
                return 0

            # 滑动窗口状态
            pending_requests = {}
            window_available = asyncio.Event()  # 窗口可用事件
            window_available.set()  # 初始窗口有空间

            # 请求者
            async def requester():
                for chunk_id in my_chunks:
                    # 等待窗口有空间（事件驱动，避免忙轮询）
                    while len(pending_requests) >= window_size:
                        window_available.clear()
                        await window_available.wait()

                    # 请求chunk
                    await socket.send_multipart([
                        b'', b'DOWNLOAD_CHUNK_CONCURRENT',
                        file_key.encode('utf-8'),
                        str(chunk_id).encode('utf-8')
                    ])

                    pending_requests[chunk_id] = time.time()

            # 接收者
            async def receiver():
                for _ in my_chunks:
                    frames = await socket.recv_multipart()
                    # 检查是否是错误响应
                    if len(frames) >= 3 and frames[1] == b'ERROR':
                        error_msg = frames[2].decode('utf-8') if len(frames) > 2 else "Unknown error"
                        raise Exception(f"下载chunk失败: {error_msg}")
                    if len(frames) < 4 or frames[1] != b'CHUNK':
                        raise Exception(f"服务器响应格式错误: {frames[1] if len(frames) > 1 else 'empty'}")

                    chunk_id = int(frames[2].decode('utf-8'))
                    chunk_data = frames[3]

                    pending_requests.pop(chunk_id, None)
                    window_available.set()  # 通知 requester 窗口有空间

                    # 背压：等待缓冲区有空间
                    while len(chunks_buffer) >= max_buffer_chunks:
                        buffer_space_available.clear()
                        await buffer_space_available.wait()

                    # 缓存chunk
                    async with buffer_lock:
                        chunks_buffer[chunk_id] = chunk_data
                    chunk_ready.set()  # 通知 writer 有新 chunk 可写

            await asyncio.gather(requester(), receiver())
            return len(my_chunks)

        # 文件写入器
        async def writer():
            nonlocal next_write_id, bytes_received

            async with aiofiles.open(output_path, 'wb') as f:
                while next_write_id < total_chunks:
                    # 等待chunk（事件驱动，避免忙轮询）
                    while next_write_id not in chunks_buffer:
                        chunk_ready.clear()
                        await chunk_ready.wait()

                    # 按序写入
                    async with buffer_lock:
                        data = chunks_buffer.pop(next_write_id)
                    buffer_space_available.set()  # 通知 receiver 缓冲区有空间

                    await f.write(data)
                    hash_obj.update(data)
                    bytes_received += len(data)
                    next_write_id += 1

                    # 调用进度回调（如果提供）
                    if progress_callback:
                        try:
                            if asyncio.iscoroutinefunction(progress_callback):
                                await progress_callback(bytes_received, file_size)
                            else:
                                progress_callback(bytes_received, file_size)
                        except Exception as e:
                            logger.warning(f"进度回调失败: {e}")

        # 并发运行
        if show_progress:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                download_task = progress.add_task(
                    f"[cyan]下载中",
                    total=file_size
                )

                async def progress_updater():
                    last_bytes = 0
                    while not download_done.is_set():
                        await asyncio.sleep(0.1)
                        if bytes_received > last_bytes:
                            progress.update(download_task, completed=bytes_received)
                            last_bytes = bytes_received
                    # 最后一次更新
                    progress.update(download_task, completed=bytes_received)

                # 启动进度更新
                progress_task = asyncio.create_task(progress_updater())

                # 运行worker和writer
                tasks = [socket_worker(i) for i in range(num_sockets)]
                tasks.append(writer())
                await asyncio.gather(*tasks)

                # 通知进度更新完成
                download_done.set()
                await progress_task
        else:
            tasks = [socket_worker(i) for i in range(num_sockets)]
            tasks.append(writer())
            await asyncio.gather(*tasks)

        # 计算详细耗时
        transfer_time = time.time() - transfer_start
        total_time = time.time() - overall_start
        prepare_time = connect_time  # 准备时间主要是连接建立

        throughput = (bytes_received / (1024 * 1024)) / transfer_time if transfer_time > 0 else 0

        if show_progress:
            from rich.table import Table
            # 4列布局（2对键值），更紧凑
            table = Table(title="[bold green]✓ 下载完成", show_header=False, border_style="green", show_edge=False, padding=(0, 1))
            table.add_column(style="dim", justify="right")
            table.add_column(style="")
            table.add_column(style="dim", justify="right")
            table.add_column(style="")

            table.add_row("文件", f"[cyan]{file_key}[/cyan]", "大小", f"[yellow]{bytes_received / (1024*1024):.2f} MB[/yellow]")
            table.add_row("保存到", f"[yellow]{output_path}[/yellow]", "", "")
            table.add_row("总耗时", f"[magenta]{total_time:.2f}秒[/magenta]", "吞吐量", f"[green]{throughput:.2f} MB/s[/green]")
            console.print(table)

        return {
            'file_key': file_key,
            'size': bytes_received,
            'transfer_time': transfer_time,
            'prepare_time': prepare_time,
            'total_time': total_time,
            'throughput': throughput,
            'num_sockets': num_sockets,
            'window_size': window_size,
            'sha256': hash_obj.hexdigest()
        }

    async def delete_file(self, file_key: str) -> bool:
        """删除文件"""
        if not self.connected or not self.sockets:
            await self.connect(1)

        await self.sockets[0].send_multipart([b'', b'DELETE', file_key.encode('utf-8')])
        frames = await self.sockets[0].recv_multipart()

        if len(frames) < 2:
            return False

        return frames[1] == b'OK'

    async def list_files(self, prefix: str = "", compute_hash: bool = False) -> list:
        """
        列出服务器上的文件

        Args:
            prefix: 文件前缀（可选，用于过滤）
            compute_hash: 是否计算文件SHA256哈希（可选，默认False，会增加性能开销）

        Returns:
            文件列表，每个文件包含 key, size, mtime, 以及可选的 sha256
        """
        if not self.connected or not self.sockets:
            await self.connect(1)

        hash_flag = b'true' if compute_hash else b'false'
        await self.sockets[0].send_multipart([b'', b'LIST', prefix.encode('utf-8'), hash_flag])
        frames = await self.sockets[0].recv_multipart()

        if len(frames) < 2:
            raise Exception("服务器响应无效")

        if frames[1] == b'ERROR':
            error_msg = frames[2].decode('utf-8') if len(frames) > 2 else "Unknown error"
            raise Exception(f"列出文件失败: {error_msg}")

        if frames[1] != b'OK':
            raise Exception(f"列出文件失败: {frames[1]}")

        # 解析文件列表
        files_json = frames[2].decode('utf-8')
        files = json.loads(files_json)

        return files

    async def close(self):
        """关闭所有连接"""
        # 设置linger=0立即关闭，避免阻塞
        for sock in self.sockets:
            sock.setsockopt(zmq.LINGER, 0)
            sock.close()

        self.sockets = []
        self.connected = False

        # 只有拥有 context 时才销毁（避免销毁共享的 context）
        if self._owns_context:
            try:
                self.context.destroy(linger=0)
            except Exception:
                pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class MultiSocketFlaxFileClientSync:
    """MultiSocketFlaxFileClient的同步包装器 - 用于CLI"""

    def __init__(
        self,
        server_host: str = "127.0.0.1",
        port: int = 25555,
        password: Optional[str] = None,
        num_connections: Optional[int] = None,
        window_size: int = 8
    ):
        from .crypto import get_password
        import sys

        # 在同步上下文中获取密码
        if password is None:
            password = get_password(
                prompt="服务器密码: ",
                allow_empty=True,
                env_var="FLAXFILE_PASSWORD",
                is_server=False
            )

        self.async_client = MultiSocketFlaxFileClient(
            server_host=server_host,
            port=port,
            password=password,
            num_connections=num_connections,
            window_size=window_size
        )

        # Windows 平台：设置事件循环策略
        if sys.platform == 'win32':
            try:
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            except AttributeError:
                pass

    def upload_file(
        self,
        file_path: str,
        file_key: str,
        chunk_size: int = 4 * 1024 * 1024,
        show_progress: bool = False,
        session_id: str = None,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """上传文件（同步接口）"""
        return asyncio.run(
            self.async_client.upload_file(file_path, file_key, chunk_size, show_progress, session_id, progress_callback)
        )

    def download_file(
        self,
        file_key: str,
        output_path: str,
        chunk_size: int = 4 * 1024 * 1024,
        show_progress: bool = False,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """下载文件（同步接口）"""
        return asyncio.run(
            self.async_client.download_file(file_key, output_path, chunk_size, show_progress, progress_callback)
        )

    def delete_file(self, file_key: str) -> bool:
        """删除文件（同步接口）"""
        return asyncio.run(self.async_client.delete_file(file_key))

    def list_files(self, prefix: str = "", compute_hash: bool = False) -> list:
        """列出文件（同步接口）"""
        return asyncio.run(self.async_client.list_files(prefix, compute_hash))

    def connect(self):
        """
        连接到服务器（空实现，为了兼容性）

        注意：MultiSocketFlaxFileClient 在每次操作时自动建立连接，
        不需要显式调用 connect()。此方法仅用于保持接口兼容。
        """
        # 空实现，因为 MultiSocketFlaxFileClient 在 upload/download 时自动连接
        pass

    def close(self):
        """关闭连接"""
        asyncio.run(self.async_client.close())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
