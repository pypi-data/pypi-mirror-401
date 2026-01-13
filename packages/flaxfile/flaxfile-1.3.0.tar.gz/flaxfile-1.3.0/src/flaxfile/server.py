#!/usr/bin/env python3
"""
FlaxFile 异步单端口服务器 - 使用 DEALER/ROUTER 模式
支持多连接 + aiofiles异步文件I/O
"""

import zmq
import zmq.asyncio
import json
import hashlib
import time
import argparse
import asyncio
import aiofiles
import shutil
from pathlib import Path
from typing import Optional, Dict
from loguru import logger
from .crypto import get_password, configure_server_encryption, get_key_fingerprint, derive_server_keypair

# 存储目录（默认值，会在服务器启动时创建）
STORAGE_DIR = Path("zmq_streaming_storage")


def _sanitize_path(base_path: Path, relative_path: str) -> Optional[Path]:
    """
    安全地构造路径，防止路径遍历攻击

    Args:
        base_path: 基础目录
        relative_path: 相对路径

    Returns:
        安全的绝对路径，如果检测到路径遍历则返回 None
    """
    try:
        # 移除开头的 /
        relative_path = relative_path.lstrip('/')

        # 构造完整路径
        full_path = (base_path / relative_path).resolve()

        # 检查是否在基础目录内
        base_resolved = base_path.resolve()
        if base_resolved in full_path.parents or full_path == base_resolved:
            return full_path
        else:
            # 路径遍历攻击
            logger.warning(f"检测到路径遍历攻击: {relative_path}")
            return None
    except (ValueError, OSError):
        return None

# 统计信息
stats = {
    'uploads': 0,
    'downloads': 0,
    'bytes_uploaded': 0,
    'bytes_downloaded': 0
}


class FlaxFileServer:
    """FlaxFile 异步单端口文件传输服务器"""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 25555,
        password: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.password = password

        self.context = zmq.asyncio.Context()
        self.socket = None

        # 新的会话管理：按 session_id 索引（支持多文件并发上传）
        self.upload_sessions: Dict[str, dict] = {}  # session_id -> session_info

        # 映射 identity 到 session_id（用于处理chunk和清理）
        self.identity_to_session: Dict[bytes, str] = {}

        # 全局锁：保护会话创建
        self.session_creation_lock = asyncio.Lock()

        # 会话超时清理任务
        self._cleanup_task: Optional[asyncio.Task] = None
        self._session_timeout = 300  # 5分钟无活动超时

    async def _cleanup_stale_sessions(self):
        """定期清理超时的上传会话（防止内存泄漏）"""
        while True:
            try:
                await asyncio.sleep(60)  # 每分钟检查一次
                now = time.time()
                stale_sessions = []

                for session_id, session in self.upload_sessions.items():
                    if now - session.get('last_activity', session['start_time']) > self._session_timeout:
                        stale_sessions.append(session_id)

                for session_id in stale_sessions:
                    session = self.upload_sessions.pop(session_id, None)
                    if session:
                        # 关闭文件并删除临时文件
                        try:
                            await session['file'].close()
                            if session['file_path'].exists():
                                session['file_path'].unlink()
                            logger.warning(f"⚠️ 清理超时会话: {session_id[:8]}... (文件: {session['file_key']})")
                        except Exception as e:
                            logger.error(f"清理会话失败: {e}")

                        # 清理 identity 映射
                        for identity in list(session.get('identities', [])):
                            self.identity_to_session.pop(identity, None)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"清理任务异常: {e}")

    def _get_optimal_chunk_size(self, file_size: int, requested_chunk_size: Optional[int] = None) -> int:
        """
        获取最优chunk大小（KISS原则：简单的自适应逻辑）

        Args:
            file_size: 文件大小
            requested_chunk_size: 客户端请求的chunk大小（可选）

        Returns:
            最优的chunk大小
        """
        if requested_chunk_size:
            return requested_chunk_size

        # 根据文件大小自适应
        if file_size < 500 * 1024 * 1024:  # < 500MB
            return 16 * 1024 * 1024  # 16MB
        else:  # >= 500MB
            return 32 * 1024 * 1024  # 32MB

    async def start(self):
        """启动服务器"""
        # 获取密码（如果未提供）
        if self.password is None:
            self.password = get_password(
                prompt="请输入服务器密码（用于加密传输）: ",
                allow_empty=True,
                env_var="FLAXFILE_PASSWORD",
                is_server=True
            )

        # 创建存储目录（只在服务器启动时创建）
        STORAGE_DIR.mkdir(exist_ok=True)

        logger.info("="*70)
        logger.info("FlaxFile 异步单端口文件传输服务器 (DEALER/ROUTER)")
        logger.info("="*70)
        logger.info(f"存储目录: {STORAGE_DIR.absolute()}")
        logger.info(f"服务地址: tcp://{self.host}:{self.port}")

        # 创建 ROUTER socket (单端口处理所有通信)
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.RCVBUF, 128 * 1024 * 1024)
        self.socket.setsockopt(zmq.SNDBUF, 128 * 1024 * 1024)
        self.socket.setsockopt(zmq.LINGER, 0)

        # 配置加密
        encryption_enabled = configure_server_encryption(self.socket, self.password)

        self.socket.bind(f"tcp://{self.host}:{self.port}")

        logger.info("="*70)
        logger.info(f"✓ 服务器已启动，监听 {self.host}:{self.port}")
        if self.host == "0.0.0.0":
            logger.warning("  监听所有网卡，允许远程连接")

        # 显示加密状态
        if encryption_enabled:
            _, server_public_key = derive_server_keypair(self.password)
            fingerprint = get_key_fingerprint(server_public_key)
            logger.info(f"🔒 已启用 CurveZMQ 加密")
            logger.info(f"   服务器公钥指纹: {fingerprint}")
        else:
            logger.warning("⚠️  未启用加密 - 数据将明文传输")
            logger.warning("   建议设置 FLAXFILE_PASSWORD 环境变量或交互输入密码")

        logger.info("="*70)
        logger.info("")

        # 启动会话超时清理任务
        self._cleanup_task = asyncio.create_task(self._cleanup_stale_sessions())

        try:
            while True:
                # 接收消息: [identity, b'', command_type, ...args]
                frames = await self.socket.recv_multipart()

                if len(frames) < 3:
                    logger.warning(f"收到无效消息: {len(frames)} frames")
                    continue

                identity = frames[0]
                # frames[1] 是空分隔符
                command = frames[2]

                # 异步处理命令
                asyncio.create_task(self.handle_command(identity, command, frames[3:]))

        except KeyboardInterrupt:
            logger.info("\n服务器停止")
        finally:
            await self.stop()

    async def handle_command(self, identity: bytes, command: bytes, args: list):
        """处理客户端命令"""
        try:
            if command == b'PING':
                await self.socket.send_multipart([identity, b'', b'PONG'])

            elif command == b'UPLOAD_START_CONCURRENT':
                await self.handle_upload_start_concurrent(identity, args)

            elif command == b'UPLOAD_CHUNK_CONCURRENT':
                await self.handle_upload_chunk_concurrent(identity, args)

            elif command == b'UPLOAD_END':
                await self.handle_upload_end(identity)

            elif command == b'DOWNLOAD_START_CONCURRENT':
                await self.handle_download_start_concurrent(identity, args)

            elif command == b'DOWNLOAD_CHUNK_CONCURRENT':
                await self.handle_download_chunk_concurrent(identity, args)

            elif command == b'DELETE':
                await self.handle_delete(identity, args)

            elif command == b'LIST':
                await self.handle_list(identity, args)

            else:
                logger.warning(f"未知命令: {command}")
                await self.socket.send_multipart([identity, b'', b'ERROR', b'Unknown command'])

        except Exception as e:
            logger.error(f"处理命令失败: {e}")
            try:
                await self.socket.send_multipart([identity, b'', b'ERROR', str(e).encode('utf-8')])
            except Exception:
                pass

    async def handle_upload_end(self, identity: bytes):
        """完成上传（支持多socket协同）"""
        if identity not in self.identity_to_session:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'No active upload'])
            return

        result = {'status': 'ok', 'message': 'Upload ended'}  # 默认result

        session_id = self.identity_to_session.get(identity)
        if session_id and session_id in self.upload_sessions:
            session = self.upload_sessions[session_id]

            # 使用会话锁保护UPLOAD_END的并发访问
            async with session['lock']:
                session['identities'].discard(identity)

                # 只有当所有identity都结束时，才真正关闭文件
                if len(session['identities']) == 0:
                    # 所有socket都完成了，关闭文件
                    await session['file'].close()  # aiofiles异步关闭

                    upload_time = time.time() - session['start_time']
                    throughput = (session['bytes_received'] / (1024 * 1024)) / upload_time if upload_time > 0 else 0

                    # 更新统计
                    stats['uploads'] += 1
                    stats['bytes_uploaded'] += session['bytes_received']

                    result = {
                        'status': 'ok',
                        'file_key': session['file_key'],
                        'size': session['bytes_received'],
                        'time': upload_time,
                        'throughput': throughput,
                        'sha256': session['hash'].hexdigest()
                    }

                    logger.info(f"✓ 上传完成 [{session_id[:8]}...]: {session['file_key']} "
                               f"({session['bytes_received']/(1024*1024):.1f} MB, "
                               f"{throughput:.2f} MB/s, "
                               f"{session['chunks_received']} chunks)")

                    # 清理会话
                    self.upload_sessions.pop(session_id)
                else:
                    # 还有其他socket在上传，只返回临时确认
                    result = {
                        'status': 'ok',
                        'message': 'Socket finished, waiting for others'
                    }
                    logger.debug(f"✓ Socket完成 [{session_id[:8]}...]: identity={identity.hex()[:8]}..., 剩余{len(session['identities'])}个")

        # 清理该identity的映射
        self.identity_to_session.pop(identity, None)

        await self.socket.send_multipart([identity, b'', b'OK', json.dumps(result).encode('utf-8')])

    async def handle_upload_start_concurrent(self, identity: bytes, args: list):
        """开始并发上传（支持多文件并发 + 单文件多socket协同）"""
        if len(args) < 4:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Missing arguments'])
            return

        session_id = args[0].decode('utf-8')  # 新增：会话ID
        file_key = args[1].decode('utf-8')
        file_size = int(args[2].decode('utf-8'))
        max_concurrency = int(args[3].decode('utf-8'))

        # 输入验证
        if len(session_id) > 256:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'session_id too long'])
            return
        if len(file_key) > 4096:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'file_key too long'])
            return
        if file_size < 0 or file_size > 10 * 1024 * 1024 * 1024 * 1024:  # 10TB上限
            await self.socket.send_multipart([identity, b'', b'ERROR', b'invalid file_size'])
            return
        if max_concurrency < 1 or max_concurrency > 1024:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'invalid max_concurrency'])
            return

        # 路径安全检查
        safe_path = _sanitize_path(STORAGE_DIR, file_key)
        if safe_path is None:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Invalid file path'])
            return

        # 使用全局锁保护会话创建
        async with self.session_creation_lock:
            # 检查是否已有该session_id的上传会话
            if session_id not in self.upload_sessions:
                # 首次上传，创建新会话
                file_path = safe_path
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # 使用aiofiles异步打开文件
                f = await aiofiles.open(file_path, 'wb')
                hash_obj = hashlib.sha256()

                logger.info(f"📤 并发上传 (session={session_id[:8]}..., x{max_concurrency}): {file_key} ({file_size/(1024*1024):.1f} MB)")

                # 按session_id索引的会话（支持多个identity共享同一session）
                self.upload_sessions[session_id] = {
                    'session_id': session_id,
                    'file_key': file_key,
                    'file_path': file_path,
                    'file': f,
                    'bytes_received': 0,
                    'expected_size': file_size,
                    'hash': hash_obj,
                    'start_time': time.time(),
                    'last_activity': time.time(),  # 最后活动时间（用于超时清理）
                    'chunks_received': 0,
                    'concurrent': True,
                    'chunks': {},  # {chunk_id: data}
                    'next_chunk_id': 0,  # 下一个要写入的chunk_id
                    'max_concurrency': max_concurrency,
                    'lock': asyncio.Lock(),  # 保护并发写入的锁
                    'identities': set()  # 参与上传的所有identity
                }
            else:
                logger.debug(f"📤 加入会话: {session_id[:8]}... (identity: {identity.hex()[:8]}...)")

            # 注册该identity到会话
            self.upload_sessions[session_id]['identities'].add(identity)
            self.identity_to_session[identity] = session_id

        await self.socket.send_multipart([identity, b'', b'OK'])

    async def handle_upload_chunk_concurrent(self, identity: bytes, args: list):
        """处理并发上传的chunk（可能乱序到达）"""
        if identity not in self.identity_to_session:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'No active upload'])
            return

        if len(args) < 2:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'No data'])
            return

        session_id = self.identity_to_session[identity]
        if session_id not in self.upload_sessions:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Session not found'])
            return

        session = self.upload_sessions[session_id]
        session['last_activity'] = time.time()  # 更新最后活动时间
        chunk_id = int(args[0].decode('utf-8'))
        data = args[1]

        # 使用锁保护并发写入的临界区
        async with session['lock']:
            # 缓存chunk（可能乱序到达）
            session['chunks'][chunk_id] = data

            # 按序写入chunk (使用aiofiles异步写入)
            while session['next_chunk_id'] in session['chunks']:
                chunk_data = session['chunks'].pop(session['next_chunk_id'])
                await session['file'].write(chunk_data)  # aiofiles异步写入
                session['hash'].update(chunk_data)
                session['bytes_received'] += len(chunk_data)
                session['chunks_received'] += 1
                session['next_chunk_id'] += 1

        # 发送ACK（带chunk_id）- 在锁外发送，避免阻塞其他chunk
        await self.socket.send_multipart([identity, b'', b'ACK', args[0]])

        # 打印进度（每10%）
        if session['expected_size'] > 0:
            progress = session['bytes_received'] / session['expected_size'] * 100
            if int(progress) % 10 == 0 and session['chunks_received'] % 100 == 1:
                logger.info(f"  进度 [{session['session_id'][:8]}...]: {progress:.0f}% ({session['bytes_received']/(1024*1024):.1f} MB)")

    async def handle_download_start_concurrent(self, identity: bytes, args: list):
        """处理并发下载开始请求（KISS优化：依赖OS页缓存）"""
        if len(args) < 1:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Missing file_key'])
            return

        file_key = args[0].decode('utf-8')
        # 支持客户端指定chunk_size（可选参数）
        requested_chunk_size = None
        if len(args) >= 2:
            try:
                requested_chunk_size = int(args[1].decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                pass

        # 路径安全检查
        file_path = _sanitize_path(STORAGE_DIR, file_key)
        if file_path is None:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Invalid file path'])
            return

        try:
            file_size = file_path.stat().st_size
        except FileNotFoundError:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'File not found'])
            return

        # 使用最优chunk_size
        chunk_size = self._get_optimal_chunk_size(file_size, requested_chunk_size)
        total_chunks = (file_size + chunk_size - 1) // chunk_size

        logger.info(f"📥 并发下载: {file_key} ({file_size/(1024*1024):.1f} MB, {total_chunks} chunks, chunk={chunk_size/(1024*1024):.0f}MB)")

        # 返回文件信息
        await self.socket.send_multipart([
            identity, b'', b'OK',
            str(file_size).encode('utf-8'),
            str(total_chunks).encode('utf-8'),
            str(chunk_size).encode('utf-8')
        ])

    async def handle_download_chunk_concurrent(self, identity: bytes, args: list):
        """处理并发下载chunk请求（KISS优化：依赖OS页缓存优化性能）"""
        if len(args) < 2:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Missing arguments'])
            return

        file_key = args[0].decode('utf-8')
        chunk_id = int(args[1].decode('utf-8'))

        # 路径安全检查
        file_path = _sanitize_path(STORAGE_DIR, file_key)
        if file_path is None:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Invalid file path'])
            return

        if not file_path.exists():
            await self.socket.send_multipart([identity, b'', b'ERROR', b'File not found'])
            return

        try:
            # 🔥 KISS原则：简化设计，每次打开文件读取
            # OS页缓存会自动优化重复读取的性能
            # 避免了复杂的会话管理和多Socket共享文件对象的问题
            file_size = file_path.stat().st_size
            chunk_size = self._get_optimal_chunk_size(file_size)

            async with aiofiles.open(file_path, 'rb') as f:
                offset = chunk_id * chunk_size

                await f.seek(offset)
                chunk_data = await f.read(chunk_size)

            # 返回chunk数据
            await self.socket.send_multipart([
                identity, b'', b'CHUNK',
                str(chunk_id).encode('utf-8'),
                chunk_data
            ])

        except Exception as e:
            logger.error(f"读取chunk失败: {e}")
            await self.socket.send_multipart([identity, b'', b'ERROR', str(e).encode('utf-8')])

    async def handle_delete(self, identity: bytes, args: list):
        """删除文件或目录"""
        if len(args) < 1:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Missing file_key'])
            return

        file_key = args[0].decode('utf-8')

        # 路径安全检查
        file_path = _sanitize_path(STORAGE_DIR, file_key)
        if file_path is None:
            await self.socket.send_multipart([identity, b'', b'ERROR', b'Invalid file path'])
            return

        try:
            if file_path.is_dir():
                # 使用线程池执行阻塞操作，避免阻塞事件循环
                def _delete_directory(path: Path) -> int:
                    """在线程中删除目录并返回大小"""
                    total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                    shutil.rmtree(path)
                    return total_size

                total_size = await asyncio.to_thread(_delete_directory, file_path)
                logger.info(f"✓ 删除目录: {file_key} ({total_size/(1024*1024):.1f} MB)")
            elif file_path.exists():
                # 删除文件（单文件删除很快，无需线程池）
                file_size = file_path.stat().st_size
                file_path.unlink()
                logger.info(f"✓ 删除文件: {file_key} ({file_size/(1024*1024):.1f} MB)")
            else:
                await self.socket.send_multipart([identity, b'', b'ERROR', b'File not found'])
                return

            await self.socket.send_multipart([identity, b'', b'OK'])
        except Exception as e:
            logger.error(f"删除失败: {e}")
            await self.socket.send_multipart([identity, b'', b'ERROR', str(e).encode('utf-8')])

    async def handle_list(self, identity: bytes, args: list):
        """列出指定前缀下的所有文件"""
        # 获取前缀（可选）
        prefix = args[0].decode('utf-8') if args else ""
        # 获取是否计算哈希（可选，默认False）
        compute_hash = args[1].decode('utf-8') == 'true' if len(args) > 1 else False

        try:
            files_info = []

            # 1. 先收集所有匹配的文件
            matched_files = []
            for file_path in STORAGE_DIR.rglob('*'):
                if file_path.is_file():
                    # 计算相对路径
                    relative_path = file_path.relative_to(STORAGE_DIR)
                    key = str(relative_path)

                    # 如果指定了前缀，只返回匹配的文件
                    if prefix:
                        # 确保前缀以 / 结尾，避免匹配到前缀相似的其他目录
                        search_prefix = prefix if prefix.endswith('/') else prefix + '/'
                        if not key.startswith(search_prefix):
                            continue

                    # 获取文件信息
                    stat = file_path.stat()
                    file_info = {
                        'key': key,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime
                    }
                    matched_files.append((file_path, file_info))

            # 2. 如果需要计算哈希，并发执行（避免串行阻塞）
            if compute_hash and matched_files:
                import aiofiles
                import xxhash

                # 并发哈希计算函数
                async def compute_file_hash(file_path: Path, semaphore: asyncio.Semaphore) -> str:
                    async with semaphore:
                        hash_obj = xxhash.xxh3_64()
                        async with aiofiles.open(file_path, 'rb') as f:
                            while True:
                                chunk = await f.read(1024 * 1024)  # 1MB chunks
                                if not chunk:
                                    break
                                hash_obj.update(chunk)
                        return hash_obj.hexdigest()

                # 限制并发数为 8，避免打开过多文件
                semaphore = asyncio.Semaphore(8)
                hash_tasks = [compute_file_hash(fp, semaphore) for fp, _ in matched_files]
                hashes = await asyncio.gather(*hash_tasks)

                # 合并哈希结果到文件信息
                for (_, file_info), file_hash in zip(matched_files, hashes):
                    file_info['hash'] = file_hash
                    files_info.append(file_info)
            else:
                # 不计算哈希，直接使用文件信息
                files_info = [file_info for _, file_info in matched_files]

            # 序列化文件列表
            import json
            files_json = json.dumps(files_info).encode('utf-8')

            hash_msg = " (含xxHash)" if compute_hash else ""
            logger.info(f"📋 列出文件: 前缀='{prefix}', 数量={len(files_info)}{hash_msg}")
            await self.socket.send_multipart([identity, b'', b'OK', files_json])

        except Exception as e:
            logger.error(f"列出文件失败: {e}")
            await self.socket.send_multipart([identity, b'', b'ERROR', str(e).encode('utf-8')])

    async def stop(self):
        """停止服务器"""
        # 取消清理任务
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        # 关闭所有活跃的上传会话
        for session in self.upload_sessions.values():
            try:
                await session['file'].close()
            except Exception:
                pass

        if self.socket:
            self.socket.close()
        self.context.term()

        logger.info("")
        logger.info("统计信息:")
        logger.info(f"  上传: {stats['uploads']} 个文件, {stats['bytes_uploaded']/(1024*1024):.1f} MB")
        logger.info(f"  下载: {stats['downloads']} 个文件, {stats['bytes_downloaded']/(1024*1024):.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="FlaxFile Server")
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind')
    parser.add_argument('--port', type=int, default=25555, help='Port to bind')
    parser.add_argument('--password', default=None, help='Password for encryption (or set FLAXFILE_PASSWORD env var)')

    args = parser.parse_args()

    server = FlaxFileServer(host=args.host, port=args.port, password=args.password)
    asyncio.run(server.start())


if __name__ == "__main__":
    main()
