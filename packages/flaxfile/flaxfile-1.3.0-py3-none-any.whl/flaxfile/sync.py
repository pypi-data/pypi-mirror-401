#!/usr/bin/env python3
"""
FlaxFile 目录同步功能
"""

import os
import asyncio
import zmq.asyncio
from pathlib import Path
from typing import List, Tuple, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TransferSpeedColumn, TimeRemainingColumn, DownloadColumn
from rich.panel import Panel
from rich.table import Table
from rich import box
import xxhash

console = Console()

# 并发上传/下载的默认配置
DEFAULT_CONCURRENCY = 32  # 默认并发数(会被自适应策略覆盖)
MAX_TOTAL_SOCKETS = 64  # 总Socket数上限（远程服务器建议不超过64）


def _format_size(bytes_size: int) -> str:
    """格式化文件大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def compute_file_hash(file_path: Path) -> str:
    """
    计算文件哈希（使用 xxHash3-64，速度快且碰撞概率极低）

    Args:
        file_path: 文件路径

    Returns:
        xxHash3-64 哈希字符串（十六进制，16字符）
    """
    hash_obj = xxhash.xxh3_64()  # 64位xxHash3，对于文件同步已足够
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024 * 1024)  # 1MB chunks
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


async def compute_file_hash_async(file_path: Path, semaphore: asyncio.Semaphore) -> str:
    """
    异步计算文件哈希（并发友好版本）

    Args:
        file_path: 文件路径
        semaphore: 并发控制信号量

    Returns:
        xxHash3-64 哈希字符串
    """
    async with semaphore:
        # 在线程池中执行 I/O 密集型操作
        return await asyncio.to_thread(compute_file_hash, file_path)


def parse_gitignore(gitignore_path: Path) -> List[str]:
    """
    解析 .gitignore 文件

    Args:
        gitignore_path: .gitignore 文件路径

    Returns:
        忽略规则列表
    """
    if not gitignore_path.exists():
        return []

    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            patterns.append(line)

    return patterns


def should_ignore(path: str, patterns: List[str], is_dir: bool = False) -> bool:
    """
    检查路径是否应该被忽略（改进版 gitignore 匹配）

    支持的模式：
    - * 匹配任意字符（除了 /）
    - ** 匹配任意字符（包括 /）
    - ? 匹配单个字符
    - [abc] 字符类
    - / 开头：仅匹配根目录
    - / 结尾：仅匹配目录
    - ! 开头：否定规则

    Args:
        path: 相对路径
        patterns: gitignore 规则列表
        is_dir: 是否为目录

    Returns:
        是否应该忽略
    """
    import fnmatch
    import re
    from functools import lru_cache

    @lru_cache(maxsize=256)
    def compile_regex(pattern_str: str):
        """缓存编译后的正则表达式"""
        return re.compile(pattern_str)

    # 跟踪最后匹配的结果（用于处理否定规则）
    last_match = False

    for pattern in patterns:
        # 处理否定规则（!）
        negate = pattern.startswith('!')
        if negate:
            pattern = pattern[1:]

        # 处理目录规则（以 / 结尾）
        pattern_is_dir = pattern.endswith('/')
        if pattern_is_dir:
            pattern = pattern[:-1]
            # 目录规则只匹配目录
            if not is_dir:
                continue

        # 处理根目录规则（以 / 开头）
        anchored = pattern.startswith('/')
        if anchored:
            pattern = pattern[1:]

        # 处理 ** 通配符
        if '**' in pattern:
            # 将 ** 转换为正则表达式
            # a/**/b 匹配 a/x/b, a/x/y/b 等
            regex_pattern = pattern.replace('**', '.*')
            # 转义其他特殊字符，但保留已转换的 .*
            parts = regex_pattern.split('.*')
            escaped_parts = [re.escape(part) for part in parts]
            regex_pattern = '.*'.join(escaped_parts)
            # 将 * 转换为 [^/]* （匹配除 / 外的任意字符）
            regex_pattern = regex_pattern.replace(r'\*', '[^/]*')
            # 将 ? 转换为 [^/]
            regex_pattern = regex_pattern.replace(r'\?', '[^/]')
            regex_pattern = f'^{regex_pattern}$'

            # 使用缓存的编译后正则表达式
            compiled_re = compile_regex(regex_pattern)
            if anchored:
                # 只匹配从根开始的路径
                matched = compiled_re.match(path) is not None
            else:
                # 匹配路径的任意部分
                matched = compiled_re.match(path) is not None or \
                         any(compiled_re.match(part) is not None
                             for part in path.split('/'))
        else:
            # 普通 fnmatch 模式
            if anchored:
                # 只匹配根目录
                matched = fnmatch.fnmatch(path, pattern)
            else:
                # 匹配任意位置
                matched = fnmatch.fnmatch(path, pattern) or \
                         fnmatch.fnmatch(path, f"*/{pattern}") or \
                         any(fnmatch.fnmatch(part, pattern)
                             for part in path.split('/'))

        if matched:
            last_match = not negate

    return last_match


def scan_directory(directory: str, respect_gitignore: bool = True) -> List[Tuple[str, str]]:
    """
    递归扫描目录，返回所有文件的相对路径

    Args:
        directory: 要扫描的目录路径
        respect_gitignore: 是否遵循 .gitignore 规则（默认 True）

    Returns:
        [(绝对路径, 相对路径), ...] 列表
    """
    directory = Path(directory).resolve()

    if not directory.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"不是目录: {directory}")

    # 解析 .gitignore
    gitignore_patterns = []
    if respect_gitignore:
        gitignore_path = directory / '.gitignore'
        gitignore_patterns = parse_gitignore(gitignore_path)

    files = []
    skipped_symlinks = []

    for root, dirs, filenames in os.walk(directory):
        root_path = Path(root)

        # 过滤目录（使用 gitignore）
        if respect_gitignore and gitignore_patterns:
            filtered_dirs = []
            for d in dirs:
                dir_path = root_path / d
                rel_path = str(dir_path.relative_to(directory))
                if not should_ignore(rel_path, gitignore_patterns, is_dir=True):
                    filtered_dirs.append(d)
            dirs[:] = filtered_dirs

        for filename in filenames:
            abs_path = Path(root) / filename

            # 处理符号链接
            if abs_path.is_symlink():
                if not abs_path.exists():
                    # 损坏的符号链接
                    rel_path = abs_path.relative_to(directory)
                    skipped_symlinks.append((str(rel_path), "损坏的符号链接"))
                    continue
                elif abs_path.is_dir():
                    # 指向目录的符号链接（跳过，避免循环）
                    rel_path = abs_path.relative_to(directory)
                    skipped_symlinks.append((str(rel_path), "指向目录的符号链接"))
                    continue
                # 指向文件的符号链接 - 允许

            # 检查文件是否存在且是文件
            if not abs_path.exists() or not abs_path.is_file():
                continue

            rel_path = abs_path.relative_to(directory)

            # 检查是否应该忽略
            if respect_gitignore and gitignore_patterns:
                if should_ignore(str(rel_path), gitignore_patterns, is_dir=False):
                    continue

            files.append((str(abs_path), str(rel_path)))

    # 输出跳过的符号链接警告
    if skipped_symlinks:
        console.print(f"[yellow]⚠️  跳过 {len(skipped_symlinks)} 个符号链接:")
        for rel_path, reason in skipped_symlinks[:5]:  # 只显示前5个
            console.print(f"  • {rel_path} ({reason})")
        if len(skipped_symlinks) > 5:
            console.print(f"  ... 还有 {len(skipped_symlinks) - 5} 个")

    return files


async def _push_directory_async(
    server_host: str,
    port: int,
    password: Optional[str],
    local_dir: str,
    remote_dir: str,
    show_progress: bool = True,
    concurrency: int = DEFAULT_CONCURRENCY,
    files_to_upload: Optional[List[Tuple[str, str]]] = None,
) -> dict:
    """
    异步上传目录（内部实现）

    注意：为了支持真正的文件级并发，每个文件使用独立的client实例。

    Args:
        server_host: 服务器地址
        port: 服务器端口
        password: 密码
        local_dir: 本地目录路径
        remote_dir: 远程目录名称
        show_progress: 是否显示进度
        concurrency: 文件级并发数（注意：每个文件内部也有多socket并发）
        files_to_upload: 要上传的文件列表（如果为None，则扫描所有文件）

    Returns:
        同步结果统计
    """
    import time
    import zmq.asyncio

    # 记录开始时间
    overall_start = time.time()

    # 1. 确定要上传的文件
    if files_to_upload is None:
        files = scan_directory(local_dir)
    else:
        files = files_to_upload

    if not files:
        return {
            'total_files': 0,
            'uploaded': 0,
            'failed': 0,
            'total_bytes': 0,
            'transfer_time': 0,
            'total_time': 0
        }

    total_bytes = sum(os.path.getsize(abs_path) for abs_path, _ in files)

    # 创建共享的 ZMQ context（避免每个文件都创建新的 context，导致资源耗尽）
    shared_context = zmq.asyncio.Context()

    # 传输开始时间（连接建立后）
    transfer_start = time.time()

    # 2. 并发上传文件（每个文件使用独立的client实例和session_id）
    uploaded = 0
    failed = 0
    failed_files = []
    bytes_uploaded = 0
    upload_lock = asyncio.Lock()  # 保护共享变量的并发修改

    async def upload_one(abs_path: str, rel_path: str, session_id: str, progress_task=None, progress_obj=None):
        """上传单个文件 - 使用独立的client实例"""
        nonlocal uploaded, failed, bytes_uploaded

        remote_key = f"{remote_dir}/{rel_path}"
        file_size = os.path.getsize(abs_path)

        # 每个文件使用独立的client实例，但共享ZMQ context（避免创建过多context导致资源耗尽）
        # 注意：目录同步时强制使用 num_connections=1，避免大量并发文件 × 多socket 导致 fd 耗尽
        from flaxfile.multi_socket_client import MultiSocketFlaxFileClient
        client = MultiSocketFlaxFileClient(
            server_host=server_host,
            port=port,
            password=password,
            num_connections=1,  # 目录同步时每文件只用1个socket，防止 Too many open files
            silent=True,  # 批量上传时不打印连接信息
            shared_context=shared_context  # 共享ZMQ context
        )

        # 定义进度回调函数，实时更新进度条
        async def on_progress(current_bytes: int, total_bytes: int):
            """实时更新进度条"""
            if progress_obj and progress_task is not None:
                # 计算当前文件的增量，更新总进度
                # bytes_uploaded 是已完成文件的总大小
                # current_bytes 是当前文件已传输的大小
                async with upload_lock:
                    # 总进度 = 已完成文件 + 当前文件进度
                    total_progress = bytes_uploaded + current_bytes
                    # 简洁显示：只显示文件计数，不显示文件名
                    progress_obj.update(
                        progress_task,
                        completed=total_progress,
                        description=f"[cyan]上传中 ({uploaded:>3}/{len(files):<3})"
                    )

        try:
            # 上传文件（带session_id和进度回调）
            await client.upload_file(abs_path, remote_key, show_progress=False, session_id=session_id, progress_callback=on_progress)

            async with upload_lock:
                uploaded += 1
                bytes_uploaded += file_size
                # 更新进度：完成后更新
                if progress_obj and progress_task is not None:
                    progress_obj.update(
                        progress_task,
                        completed=bytes_uploaded,
                        description=f"[cyan]上传中 ({uploaded}/{len(files)})"
                    )

        except Exception as e:
            async with upload_lock:
                failed += 1
                failed_files.append((rel_path, str(e)))
            # 失败时打印到单独一行，不干扰进度条
            if progress_obj:
                progress_obj.console.print(f"[red]✗ 上传失败: {rel_path} - {e}")
            else:
                console.print(f"[red]✗ 上传失败: {rel_path} - {e}")
        finally:
            # 关闭client连接
            await client.close()

    # 3. 并发上传文件（使用信号量控制并发数）
    # 每个文件使用唯一的session_id，支持多文件并发上传
    import uuid
    semaphore = asyncio.Semaphore(concurrency)

    async def upload_with_semaphore(abs_path: str, rel_path: str, progress_task=None, progress_obj=None):
        """带信号量控制的上传"""
        session_id = str(uuid.uuid4())  # 每个文件唯一的session_id
        async with semaphore:
            await upload_one(abs_path, rel_path, session_id, progress_task, progress_obj)

    try:
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
                main_task = progress.add_task(f"[cyan]上传中 (0/{len(files)})", total=total_bytes)

                # 并发上传（最多 concurrency 个文件同时上传）
                tasks = [upload_with_semaphore(abs_path, rel_path, main_task, progress) for abs_path, rel_path in files]
                await asyncio.gather(*tasks)
        else:
            # 无进度条模式，并发上传
            tasks = [upload_with_semaphore(abs_path, rel_path) for abs_path, rel_path in files]
            await asyncio.gather(*tasks)

        # 计算耗时
        transfer_time = time.time() - transfer_start
        total_time = time.time() - overall_start
        prepare_time = transfer_start - overall_start

        return {
            'total_files': len(files),
            'uploaded': uploaded,
            'failed': failed,
            'failed_files': failed_files,
            'total_bytes': total_bytes,
            'transfer_time': transfer_time,
            'prepare_time': prepare_time,
            'total_time': total_time,
            'concurrency': concurrency
        }
    finally:
        # 清理共享的 ZMQ context
        try:
            shared_context.destroy(linger=0)
        except Exception:
            pass


def push_directory(
    client,
    local_dir: str,
    remote_dir: str,
    show_progress: bool = True,
    password: Optional[str] = None,
    force: bool = False,
    delete: bool = False,
    concurrency: int = DEFAULT_CONCURRENCY,
    max_concurrency: int = MAX_TOTAL_SOCKETS,
) -> dict:
    """
    上传本地目录到服务器（增量同步）

    默认只上传新增或修改的文件（基于SHA256比较）。

    注意：支持文件级并发（默认32个文件）+ 每个文件内部多Socket并发传输

    Args:
        client: MultiSocketFlaxFileClientSync 实例
        local_dir: 本地目录路径
        remote_dir: 远程目录名称
        show_progress: 是否显示进度
        password: 密码（可选）
        force: 强制全量同步，忽略增量比较（默认 False）
        delete: 删除远程多余的文件（默认 False）
        concurrency: 文件级并发数（默认 32）
        max_concurrency: 最大并发数限制（默认 64，可手动指定更高值如 256）

    Returns:
        同步结果统计
    """
    # 1. 显示同步任务头部（简洁单行）
    console.print()
    console.print(f"[bold cyan]上传同步:[/bold cyan] [yellow]{local_dir}[/yellow] [dim]→[/dim] [yellow]{remote_dir}[/yellow]")

    # 2. 扫描本地目录
    files = None
    remote_files_dict = {}
    files_to_upload = []

    with console.status("[cyan]分析中...", spinner="dots"):
        files = scan_directory(local_dir)

        if not files:
            console.print("[yellow]⚠️  目录为空，没有文件需要上传")
            return {
                'total_files': 0,
                'uploaded': 0,
                'failed': 0,
                'total_bytes': 0
            }

        local_count = len(files)

        # 获取远程文件列表（用于增量比较）
        if not force:
            try:
                # 请求服务器计算文件哈希
                remote_files = client.list_files(prefix=remote_dir, compute_hash=True)
                # 构建远程文件字典：{相对路径: {size, sha256, ...}}
                for rf in remote_files:
                    if rf['key'].startswith(remote_dir + '/'):
                        rel_path = rf['key'][len(remote_dir) + 1:]
                        remote_files_dict[rel_path] = rf
            except Exception as e:
                console.print(f"[yellow]⚠️  无法获取远程文件列表: {e}")
                console.print(f"[yellow]   将执行全量上传")
                force = True

    # 3. 增量比较：决定哪些文件需要上传（基于 SHA256）
    skipped = 0
    new_files = 0
    modified_files = 0

    if force:
        # 强制模式：上传所有文件
        files_to_upload = files
        console.print(f"[bold yellow]强制模式[/bold yellow]：将上传所有文件")
    else:
        # 增量模式：只上传新增或修改的文件（基于 xxHash 比较）
        # 1. 先分类文件：新文件、需要哈希比较的文件、按大小比较的文件
        new_file_list = []
        files_needing_hash = []  # [(abs_path, rel_path, remote_hash), ...]
        files_by_size = []  # [(abs_path, rel_path, remote_size), ...]

        for abs_path, rel_path in files:
            if rel_path not in remote_files_dict:
                new_file_list.append((abs_path, rel_path))
            else:
                remote_hash = remote_files_dict[rel_path].get('hash')
                if remote_hash:
                    files_needing_hash.append((abs_path, rel_path, remote_hash))
                else:
                    files_by_size.append((abs_path, rel_path, remote_files_dict[rel_path]['size']))

        # 2. 并发计算需要哈希比较的文件（使用线程池）
        local_hashes = {}
        if files_needing_hash:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "[cyan]计算xxHash (并发)...",
                    total=len(files_needing_hash)
                )

                # 使用线程池并发计算哈希（最多 8 个线程）
                with ThreadPoolExecutor(max_workers=8) as executor:
                    future_to_file = {
                        executor.submit(compute_file_hash, Path(abs_path)): (abs_path, rel_path)
                        for abs_path, rel_path, _ in files_needing_hash
                    }

                    completed_count = 0
                    for future in as_completed(future_to_file):
                        abs_path, rel_path = future_to_file[future]
                        try:
                            local_hashes[rel_path] = future.result()
                        except Exception as e:
                            # 哈希计算失败，当作需要上传
                            local_hashes[rel_path] = None
                        completed_count += 1
                        progress.update(task, completed=completed_count)

        # 3. 汇总结果
        # 新文件
        for abs_path, rel_path in new_file_list:
            files_to_upload.append((abs_path, rel_path))
            new_files += 1

        # 需要哈希比较的文件
        for abs_path, rel_path, remote_hash in files_needing_hash:
            local_hash = local_hashes.get(rel_path)
            if local_hash is None or local_hash != remote_hash:
                files_to_upload.append((abs_path, rel_path))
                modified_files += 1
            else:
                skipped += 1

        # 按大小比较的文件
        for abs_path, rel_path, remote_size in files_by_size:
            local_size = os.path.getsize(abs_path)
            if local_size != remote_size:
                files_to_upload.append((abs_path, rel_path))
                modified_files += 1
            else:
                skipped += 1

        # 显示增量分析结果（简洁版，包含本地和远程文件数）
        remote_count = len(remote_files_dict)
        console.print(f"[green]✓[/green] 分析完成: [green]{new_files} 个新增[/green], [yellow]{modified_files} 个修改[/yellow], [dim]{skipped} 个跳过[/dim] [dim](本地 {local_count} 个, 远程 {remote_count} 个)[/dim]")

    # 4. 处理删除（可选）
    deleted = 0
    if delete and remote_files_dict:
        local_files_set = {rel_path for _, rel_path in files}
        files_to_delete = [rp for rp in remote_files_dict.keys() if rp not in local_files_set]

        if files_to_delete:
            console.print(f"\n[yellow]发现 {len(files_to_delete)} 个远程多余文件，正在删除...")
            for remote_rel_path in files_to_delete:
                remote_key = f"{remote_dir}/{remote_rel_path}"
                try:
                    client.delete_file(remote_key)
                    console.print(f"  [dim]✓ 删除: {remote_rel_path}[/dim]")
                    deleted += 1
                except Exception as e:
                    console.print(f"  [red]✗ 删除失败: {remote_rel_path} - {e}[/red]")
            console.print(f"[green]✓ 已删除 {deleted} 个远程文件[/green]")

    # 5. 检查是否有文件需要上传
    if not files_to_upload:
        console.print()
        console.print("[bold green]✓ 所有文件已是最新，无需上传[/bold green]")
        return {
            'total_files': len(files),
            'uploaded': 0,
            'failed': 0,
            'skipped': skipped,
            'deleted': deleted,
            'total_bytes': 0
        }

    # 6. 计算需要上传的总大小和显示传输计划
    total_bytes = sum(os.path.getsize(abs_path) for abs_path, _ in files_to_upload)

    # 7. 自适应计算并发数（如果使用默认值）
    if concurrency == DEFAULT_CONCURRENCY:
        # 内联自适应计算，使用 max_concurrency 作为上限
        file_sizes = sorted([os.path.getsize(abs_path) for abs_path, _ in files_to_upload])
        p90_index = min(int(len(file_sizes) * 0.9), len(file_sizes) - 1)
        p90_size = file_sizes[p90_index]

        if p90_size < 1 * 1024 * 1024:  # <1MB
            adaptive_concurrency = min(max_concurrency, len(files_to_upload))
        elif p90_size < 10 * 1024 * 1024:  # 1-10MB
            adaptive_concurrency = min(max_concurrency, 64)
        elif p90_size < 100 * 1024 * 1024:  # 10-100MB
            adaptive_concurrency = min(max_concurrency, 32)
        else:  # >=100MB
            adaptive_concurrency = min(max_concurrency, 16)
    else:
        adaptive_concurrency = concurrency

    # 显示传输计划（简洁版，移除技术细节）
    console.print()
    console.print(f"[cyan]上传 {len(files_to_upload)} 个文件 ({_format_size(total_bytes)})[/cyan]")

    # 8. 调用异步实现（只上传需要的文件）
    # 传递连接参数而不是client实例，让每个文件创建独立的client
    result = asyncio.run(_push_directory_async(
        server_host=client.async_client.server_host,
        port=client.async_client.port,
        password=client.async_client.password,
        local_dir=local_dir,
        remote_dir=remote_dir,
        show_progress=show_progress,
        concurrency=adaptive_concurrency,
        files_to_upload=files_to_upload  # 只上传这些文件
    ))

    # 9. 显示结果（详细指标）
    console.print()

    if result['failed'] == 0:
        # 成功完成 - 使用Rich Table显示详细指标（4列布局）
        from rich.table import Table

        # 计算吞吐量
        transfer_time = result.get('transfer_time', 0)
        total_bytes = result.get('total_bytes', 0)
        throughput = (total_bytes / (1024 * 1024)) / transfer_time if transfer_time > 0 else 0

        table = Table(title="[bold green]✓ 同步上传完成", show_header=False, border_style="green", show_edge=False, padding=(0, 1))
        table.add_column(style="dim", justify="right")
        table.add_column(style="")
        table.add_column(style="dim", justify="right")
        table.add_column(style="")

        table.add_row("本地", f"[yellow]{local_dir}[/yellow]", "远程", f"[yellow]{remote_dir}[/yellow]")

        # 构建文件统计信息
        file_stats = f"[green]{result['uploaded']}[/green]"
        if not force and skipped > 0:
            file_stats += f" / [dim]跳过{skipped}[/dim]"
        if deleted > 0:
            file_stats += f" / [red]删除{deleted}[/red]"

        table.add_row("文件", file_stats + " 个", "数据", f"[yellow]{_format_size(total_bytes)}[/yellow]")
        table.add_row("总耗时", f"[magenta]{result.get('total_time', 0):.2f}秒[/magenta]", "吞吐量", f"[green]{throughput:.2f} MB/s[/green]")
        console.print(table)
    else:
        # 有失败
        console.print(f"[bold yellow]⚠️  同步完成（{result['failed']} 个文件失败）[/bold yellow]")
        console.print("[red]失败的文件:[/red]")
        for rel_path, error in result['failed_files']:
            console.print(f"  [red]✗ {rel_path}:[/red] {error}")

    # 添加增量同步统计信息
    result['skipped'] = skipped
    result['deleted'] = deleted
    result['new_files'] = new_files if not force else 0
    result['modified_files'] = modified_files if not force else 0

    return result


def _sanitize_path(base_path: Path, relative_path: str) -> Optional[Path]:
    """
    安全地构造路径，防止路径遍历攻击

    Args:
        base_path: 基础目录
        relative_path: 相对路径

    Returns:
        安全的绝对路径，如果检测到路径遍历则返回 None
    """
    # 规范化相对路径，移除 .. 和 .
    try:
        # 移除开头的 /
        relative_path = relative_path.lstrip('/')

        # 构造完整路径
        full_path = (base_path / relative_path).resolve()

        # 检查是否在基础目录内
        if base_path.resolve() in full_path.parents or full_path == base_path.resolve():
            return full_path
        else:
            # 路径遍历攻击
            return None
    except (ValueError, OSError):
        return None


async def _pull_directory_async(
    server_host: str,
    port: int,
    password: Optional[str],
    remote_dir: str,
    local_dir: str,
    show_progress: bool = True,
    concurrency: int = DEFAULT_CONCURRENCY,
    files_to_download: Optional[List[dict]] = None,
) -> dict:
    """
    异步下载目录（内部实现）

    Args:
        server_host: 服务器地址
        port: 服务器端口
        password: 密码（可选）
        remote_dir: 远程目录名称
        local_dir: 本地目录路径
        show_progress: 是否显示进度
        concurrency: 并发数
        files_to_download: 要下载的文件列表（必须提供）

    Returns:
        同步结果统计
    """
    import time

    # 记录开始时间
    overall_start = time.time()

    # 使用提供的文件列表
    if files_to_download is None or not files_to_download:
        return {
            'total_files': 0,
            'downloaded': 0,
            'failed': 0,
            'total_bytes': 0,
            'transfer_time': 0,
            'total_time': 0
        }

    files = files_to_download
    total_bytes = sum(f['size'] for f in files)
    local_dir_path = Path(local_dir)
    local_dir_path.mkdir(parents=True, exist_ok=True)

    # 创建共享的 ZMQ context（避免每个文件都创建新的 context，导致资源耗尽）
    shared_context = zmq.asyncio.Context()

    # 传输开始时间
    transfer_start = time.time()

    # 2. 并发下载文件（每个文件使用独立的client实例，与push保持一致）
    downloaded = 0
    failed = 0
    failed_files = []
    bytes_downloaded = 0
    download_lock = asyncio.Lock()  # 添加锁保护并发修改

    async def download_one(file_info: dict, progress_task=None, progress_obj=None):
        """下载单个文件 - 使用独立的client实例"""
        nonlocal downloaded, failed, bytes_downloaded

        remote_key = file_info['key']
        file_size = file_info['size']

        # 计算本地路径
        if remote_key.startswith(remote_dir + '/'):
            rel_path = remote_key[len(remote_dir) + 1:]
        else:
            rel_path = remote_key

        # 安全检查
        local_path = _sanitize_path(local_dir_path, rel_path)
        if local_path is None:
            async with download_lock:
                failed += 1
                failed_files.append((rel_path, "路径遍历攻击检测"))
            console.print(f"[red]✗ 跳过危险路径: {rel_path}")
            return

        # 每个文件使用独立的client实例，但共享ZMQ context
        from flaxfile.multi_socket_client import MultiSocketFlaxFileClient
        client = MultiSocketFlaxFileClient(
            server_host=server_host,
            port=port,
            password=password,
            num_connections=1,  # 目录同步时每文件只用1个socket，防止 Too many open files
            silent=True,  # 批量下载时不打印连接信息
            shared_context=shared_context  # 共享ZMQ context
        )

        # 定义进度回调函数，实时更新进度条
        async def on_progress(current_bytes: int, total_bytes: int):
            """实时更新进度条"""
            if progress_obj and progress_task is not None:
                # 计算当前文件的增量，更新总进度
                async with download_lock:
                    # 总进度 = 已完成文件 + 当前文件进度
                    total_progress = bytes_downloaded + current_bytes
                    # 简洁显示：不显示文件名
                    progress_obj.update(
                        progress_task,
                        completed=total_progress,
                        description=f"[cyan]下载中 ({downloaded:>3}/{len(files):<3})"
                    )

        # 创建父目录
        local_path.parent.mkdir(parents=True, exist_ok=True)

        # 重试机制：最多重试3次
        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                # 下载文件（带进度回调）
                await client.download_file(remote_key, str(local_path), show_progress=False, progress_callback=on_progress)

                async with download_lock:
                    downloaded += 1
                    bytes_downloaded += file_size
                    if progress_obj and progress_task is not None:
                        progress_obj.update(progress_task, completed=bytes_downloaded,
                                           description=f"[cyan]下载中 ({downloaded}/{len(files)})")
                break  # 成功，退出重试循环

            except Exception as e:
                last_error = e
                await client.close()
                if attempt < max_retries - 1:
                    # 重新创建 client 进行重试
                    client = MultiSocketFlaxFileClient(
                        server_host=server_host,
                        port=port,
                        password=password,
                        num_connections=1,
                        silent=True,
                        shared_context=shared_context
                    )
                    await asyncio.sleep(0.5 * (attempt + 1))  # 递增延迟
                else:
                    # 最后一次重试也失败
                    async with download_lock:
                        failed += 1
                        failed_files.append((rel_path, str(last_error)))
                    console.print(f"[red]✗ 下载失败: {rel_path} - {last_error}")
                    return  # 提前返回，不执行 finally 中的 close

        await client.close()

    # 3. 并发下载文件（使用信号量控制并发数，与 push 保持一致）
    semaphore = asyncio.Semaphore(concurrency)

    async def download_with_semaphore(file_info: dict, progress_task=None, progress_obj=None):
        """带信号量控制的下载"""
        async with semaphore:
            await download_one(file_info, progress_task, progress_obj)

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
            main_task = progress.add_task(f"[cyan]下载 {remote_dir}/", total=total_bytes)

            # 并发下载（最多 concurrency 个文件同时下载）
            tasks = [download_with_semaphore(fi, main_task, progress) for fi in files]
            await asyncio.gather(*tasks)
    else:
        # 无进度条模式，并发下载
        tasks = [download_with_semaphore(fi) for fi in files]
        await asyncio.gather(*tasks)

    # 计算耗时
    transfer_time = time.time() - transfer_start
    total_time = time.time() - overall_start
    prepare_time = transfer_start - overall_start

    # 清理共享的 ZMQ context
    try:
        shared_context.destroy(linger=0)
    except Exception:
        pass

    return {
        'total_files': len(files),
        'downloaded': downloaded,
        'failed': failed,
        'failed_files': failed_files,
        'total_bytes': total_bytes,
        'transfer_time': transfer_time,
        'prepare_time': prepare_time,
        'total_time': total_time
    }


def pull_directory(
    client,
    remote_dir: str,
    local_dir: str,
    show_progress: bool = True,
    password: Optional[str] = None,
    force: bool = False,
    delete: bool = False,
    concurrency: int = DEFAULT_CONCURRENCY,
    max_concurrency: int = MAX_TOTAL_SOCKETS,
) -> dict:
    """
    从服务器下载目录到本地（增量同步）

    默认只下载缺失或修改的文件（基于SHA256比较）。

    支持文件级并发下载，每个文件使用独立的连接。

    Args:
        client: MultiSocketFlaxFileClientSync 实例
        remote_dir: 远程目录名称
        local_dir: 本地目录路径
        show_progress: 是否显示进度
        password: 密码（可选）
        force: 强制全量同步，忽略增量比较（默认 False）
        delete: 删除本地多余的文件（默认 False）
        concurrency: (已弃用) 保留用于向后兼容

    Returns:
        同步结果统计
    """
    # 1. 显示同步任务头部（简洁单行）
    console.print()
    console.print(f"[bold cyan]下载同步:[/bold cyan] [yellow]{remote_dir}[/yellow] [dim]→[/dim] [yellow]{local_dir}[/yellow]")

    # 2. 获取远程文件列表
    remote_files = None
    with console.status("[cyan]分析中...", spinner="dots"):
        try:
            # 请求服务器计算文件的 SHA256 哈希
            remote_files = client.list_files(prefix=remote_dir, compute_hash=True)
        except Exception as e:
            console.print(f"[red]✗ 获取文件列表失败: {e}")
            return {
                'total_files': 0,
                'downloaded': 0,
                'failed': 0,
                'total_bytes': 0
            }

        if not remote_files:
            console.print("[yellow]⚠️  远程目录为空或不存在")
            return {
                'total_files': 0,
                'downloaded': 0,
                'failed': 0,
                'total_bytes': 0
            }

        remote_count = len(remote_files)

    # 3. 扫描本地文件（用于增量比较，计算哈希）
    local_dir_path = Path(local_dir)
    local_files_dict = {}
    files_to_download = []

    if not force and local_dir_path.exists():
        # 先收集所有本地文件
        local_files_list = []
        for root, _, filenames in os.walk(local_dir_path):
            for filename in filenames:
                abs_path = Path(root) / filename
                if abs_path.exists() and abs_path.is_file():
                    rel_path = abs_path.relative_to(local_dir_path)
                    local_files_list.append((abs_path, str(rel_path)))

        if local_files_list:
            # 使用渐进式进度条计算哈希
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "[cyan]分析差异 (计算xxHash)...",
                    total=len(local_files_list)
                )

                for idx, (abs_path, rel_path) in enumerate(local_files_list):
                    # 更新进度描述
                    progress.update(
                        task,
                        completed=idx,
                        description=f"[cyan]分析差异 ({idx}/{len(local_files_list)}) [dim]{rel_path[:40]}..."
                    )

                    # 计算哈希
                    local_hash = compute_file_hash(abs_path)
                    local_files_dict[rel_path] = local_hash

                # 完成进度
                progress.update(task, completed=len(local_files_list), description="[cyan]分析完成")

    # 4. 增量比较：决定哪些文件需要下载（基于 xxHash）
    skipped = 0
    new_files = 0
    modified_files = 0

    if force:
        # 强制模式：下载所有文件
        files_to_download = remote_files
        console.print(f"[bold yellow]强制模式[/bold yellow]：将下载所有文件")
    else:
        # 增量模式：只下载缺失或修改的文件（基于 xxHash 比较）
        for rf in remote_files:
            # 计算相对路径
            if rf['key'].startswith(remote_dir + '/'):
                rel_path = rf['key'][len(remote_dir) + 1:]
            else:
                rel_path = rf['key']

            remote_hash = rf.get('hash')

            if rel_path not in local_files_dict:
                # 新文件（本地没有）
                files_to_download.append(rf)
                new_files += 1
            else:
                # 文件存在，比较哈希
                local_hash = local_files_dict[rel_path]

                if remote_hash:
                    if local_hash != remote_hash:
                        # 哈希不同，认为已修改
                        files_to_download.append(rf)
                        modified_files += 1
                    else:
                        # 哈希相同，跳过
                        skipped += 1
                else:
                    # 远程没有哈希，根据大小判断
                    local_size = Path(local_dir_path / rel_path).stat().st_size
                    remote_size = rf['size']
                    if local_size != remote_size:
                        files_to_download.append(rf)
                        modified_files += 1
                    else:
                        skipped += 1

        # 显示增量分析结果（简洁版，包含本地和远程文件数）
        local_count = len(local_files_dict)
        console.print(f"[green]✓[/green] 分析完成: [green]{new_files} 个新增[/green], [yellow]{modified_files} 个修改[/yellow], [dim]{skipped} 个跳过[/dim] [dim](远程 {remote_count} 个, 本地 {local_count} 个)[/dim]")

    # 5. 处理删除（可选）
    deleted = 0
    if delete and local_files_dict:
        remote_files_set = set()
        for rf in remote_files:
            if rf['key'].startswith(remote_dir + '/'):
                rel_path = rf['key'][len(remote_dir) + 1:]
                remote_files_set.add(rel_path)

        files_to_delete = [lp for lp in local_files_dict.keys() if lp not in remote_files_set]

        if files_to_delete:
            console.print(f"\n[yellow]发现 {len(files_to_delete)} 个本地多余文件，正在删除...")
            for local_rel_path in files_to_delete:
                local_path = local_dir_path / local_rel_path
                try:
                    local_path.unlink()
                    console.print(f"  [dim]✓ 删除: {local_rel_path}[/dim]")
                    deleted += 1
                except Exception as e:
                    console.print(f"  [red]✗ 删除失败: {local_rel_path} - {e}[/red]")
            console.print(f"[green]✓ 已删除 {deleted} 个本地文件[/green]")

    # 6. 检查是否有文件需要下载
    if not files_to_download:
        console.print()
        console.print("[bold green]✓ 所有文件已是最新，无需下载[/bold green]")
        return {
            'total_files': len(remote_files),
            'downloaded': 0,
            'failed': 0,
            'skipped': skipped,
            'deleted': deleted,
            'total_bytes': 0
        }

    # 7. 计算需要下载的总大小和显示下载计划（简洁版）
    total_bytes = sum(f['size'] for f in files_to_download)
    console.print()
    console.print(f"[cyan]下载 {len(files_to_download)} 个文件 ({_format_size(total_bytes)})[/cyan]")

    # 7.5 自适应计算并发数（如果使用默认值）
    if concurrency == DEFAULT_CONCURRENCY:
        # 根据文件大小分布计算合适的并发数
        file_sizes = sorted([f['size'] for f in files_to_download])
        if file_sizes:
            p90_index = min(int(len(file_sizes) * 0.9), len(file_sizes) - 1)
            p90_size = file_sizes[p90_index]

            if p90_size < 1 * 1024 * 1024:  # <1MB
                concurrency = min(max_concurrency, len(files_to_download))
            elif p90_size < 10 * 1024 * 1024:  # 1-10MB
                concurrency = min(max_concurrency, 64)
            elif p90_size < 100 * 1024 * 1024:  # 10-100MB
                concurrency = min(max_concurrency, 32)
            else:  # >=100MB
                concurrency = min(max_concurrency, 16)

    # 8. 调用异步实现（只下载需要的文件）
    # 从 client 获取服务器配置
    server_host = client.async_client.server_host
    port = client.async_client.port
    client_password = client.async_client.password

    result = asyncio.run(_pull_directory_async(
        server_host=server_host,
        port=port,
        password=client_password,
        remote_dir=remote_dir,
        local_dir=local_dir,
        show_progress=show_progress,
        concurrency=concurrency,  # 使用自适应并发数
        files_to_download=files_to_download  # 只下载这些文件
    ))

    # 9. 显示结果（详细指标）
    console.print()

    if result['failed'] == 0:
        # 成功完成 - 使用Rich Table显示详细指标（4列布局）
        from rich.table import Table

        # 计算吞吐量
        transfer_time = result.get('transfer_time', 0)
        total_bytes = result.get('total_bytes', 0)
        throughput = (total_bytes / (1024 * 1024)) / transfer_time if transfer_time > 0 else 0

        table = Table(title="[bold green]✓ 同步下载完成", show_header=False, border_style="green", show_edge=False, padding=(0, 1))
        table.add_column(style="dim", justify="right")
        table.add_column(style="")
        table.add_column(style="dim", justify="right")
        table.add_column(style="")

        table.add_row("远程", f"[yellow]{remote_dir}[/yellow]", "本地", f"[yellow]{local_dir}[/yellow]")

        # 构建文件统计信息
        file_stats = f"[green]{result['downloaded']}[/green]"
        if not force and skipped > 0:
            file_stats += f" / [dim]跳过{skipped}[/dim]"
        if deleted > 0:
            file_stats += f" / [red]删除{deleted}[/red]"

        table.add_row("文件", file_stats + " 个", "数据", f"[yellow]{_format_size(total_bytes)}[/yellow]")
        table.add_row("总耗时", f"[magenta]{result.get('total_time', 0):.2f}秒[/magenta]", "吞吐量", f"[green]{throughput:.2f} MB/s[/green]")
        console.print(table)
    else:
        # 有失败
        console.print(f"[bold yellow]⚠️  同步完成（{result['failed']} 个文件失败）[/bold yellow]")
        console.print("[red]失败的文件:[/red]")
        for rel_path, error in result['failed_files']:
            console.print(f"  [red]✗ {rel_path}:[/red] {error}")

    # 添加增量同步统计信息
    result['skipped'] = skipped
    result['deleted'] = deleted
    result['new_files'] = new_files if not force else 0
    result['modified_files'] = modified_files if not force else 0

    return result
