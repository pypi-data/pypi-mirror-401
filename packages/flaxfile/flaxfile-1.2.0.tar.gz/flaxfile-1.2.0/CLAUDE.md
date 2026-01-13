# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

FlaxFile 是一个基于 ZeroMQ 的高性能跨网络文件传输系统，使用 Python 开发。主要特点：
- 异步单端口架构（基于 DEALER/ROUTER 模式）
- 多Socket并发传输 + 滑动窗口协议，上传/下载速度可达 1.5+ GB/s
- 支持 CurveZMQ (NaCl) 加密传输
- 支持文件和目录的增量同步（基于 xxHash3-64）
- Rich 终端界面显示进度

## 开发环境

### 安装依赖
```bash
# 从源码安装开发环境
pip install -e .
```

### 主要依赖
- `pyzmq>=25.0.0` - ZeroMQ Python 绑定
- `aiofiles>=23.0.0` - 异步文件 I/O
- `rich>=13.0.0` - 终端美化界面
- `PyNaCl>=1.5.0` - 加密支持
- `xxhash>=3.0.0` - 快速哈希计算
- `fire>=0.5.0` - CLI 框架

### 运行测试
```bash
pytest tests/  # 如果有测试目录
```

## 命令行工具

### 服务器操作
```bash
# 启动服务器（使用配置文件或默认配置）
flaxfile serve

# 指定地址和端口
flaxfile serve --host 0.0.0.0 --port 25555

# 启用加密
export FLAXFILE_PASSWORD="your_password"
flaxfile serve
```

### 客户端操作
```bash
# 上传文件
flaxfile set /path/to/file.bin [key]

# 下载文件
flaxfile get key [output_path]

# 列出文件（聚合视图，按顶层key显示）
flaxfile list [prefix]
flaxfile list --detailed  # 详细文件列表

# 删除文件
flaxfile delete key

# 目录同步（直接使用push/pull，无需sync前缀）
flaxfile push /local/dir [remote_dir]
flaxfile pull remote_dir [/local/dir]

# 配置管理
flaxfile config init      # 创建配置文件
flaxfile config show      # 查看配置
flaxfile config           # 交互式配置
```

## 代码架构

### 核心模块

#### 1. `server.py` - 异步单端口服务器
- **FlaxFileServer** 类：基于 ROUTER socket 的异步服务器
- 会话管理：
  - `upload_sessions`: 按 session_id 索引的上传会话（支持多文件并发 + 单文件多socket协同）
  - `identity_to_session`: 映射 ZMQ identity 到 session_id
- 核心协议：
  - `UPLOAD_START_CONCURRENT` / `UPLOAD_CHUNK_CONCURRENT` / `UPLOAD_END` - 并发上传流程
  - `DOWNLOAD_START_CONCURRENT` / `DOWNLOAD_CHUNK_CONCURRENT` - 并发下载流程
  - `LIST` - 文件列表（支持前缀过滤和可选的哈希计算）
  - `DELETE` - 文件删除
- 关键特性：
  - 使用 aiofiles 异步 I/O，避免阻塞事件循环
  - 每个上传会话都有独立的锁（`asyncio.Lock()`）保护并发写入
  - 乱序 chunk 缓存机制：按序写入文件，确保数据正确性

#### 2. `multi_socket_client.py` - 多Socket客户端
- **MultiSocketFlaxFileClient** 类：异步客户端（推荐使用）
- **MultiSocketFlaxFileClientSync** 类：同步包装器（简单场景）
- 自适应传输策略（根据文件大小选择最优Socket数量和窗口大小）：
  - < 50MB: 1个Socket，窗口16
  - 50MB - 200MB: 2个Socket，窗口8
  - 200MB - 1GB: 4个Socket，窗口8
  - \> 1GB: 8个Socket，窗口8
- 滑动窗口协议：多个 chunk 并发传输，每个 chunk 都有 ACK 确认

#### 3. `sync.py` - 目录同步
- **push_directory** / **pull_directory**: 增量同步函数
- 自适应文件级并发（基于第90百分位文件大小）：
  - 总Socket数守恒：`file_concurrency × sockets_per_file ≈ MAX_TOTAL_SOCKETS (256)`
  - < 1MB: 并发256，每文件1个socket
  - 1-10MB: 并发64，每文件4个socket
  - 10-100MB: 并发32，每文件8个socket
  - 100MB-1GB: 并发16，每文件16个socket
  - \>= 1GB: 并发16，每文件16个socket
- 增量同步逻辑：
  - 使用 xxHash3-64 快速比较文件是否相同
  - 支持 `--force` 全量同步
  - 支持 `--delete` 删除远程/本地多余文件
- .gitignore 支持：自动忽略 .git、__pycache__、node_modules 等

#### 4. `cli.py` - 命令行界面
- **FlaxFileCLI** 类：主CLI入口，包含所有顶层命令（set/get/push/pull/list/delete/serve）
- **ConfigCommands** 类：配置管理（init/show/interactive）
- 使用 `python-fire` 实现CLI路由
- 命令层级扁平化：所有命令都在顶层（如 `flaxfile push` 而非 `flaxfile sync push`）

#### 5. `config.py` - 配置管理
- 支持 TOML 格式配置文件
- 配置文件搜索路径（优先级从高到低）：
  1. `./flaxfile.toml` (当前目录)
  2. `~/flaxfile.toml` (家目录)
- 配置结构：
  - `[server]`: 服务器配置（host/port/storage_dir）
  - `[client]`: 客户端默认服务器
  - `[servers.*]`: 远程服务器列表

#### 6. `crypto.py` - 加密支持
- CurveZMQ (NaCl) 加密
- 密码派生服务器密钥对（使用 PBKDF2）
- 环境变量支持：`FLAXFILE_PASSWORD`

### 数据流设计

#### 上传流程（多Socket协同）
```
Client                                Server
  |                                      |
  |-- UPLOAD_START_CONCURRENT --------->| (创建/加入会话)
  |<-- OK -----------------------------|
  |                                      |
  |-- UPLOAD_CHUNK_CONCURRENT (0) ----->| (缓存chunk，按序写入)
  |<-- ACK (0) -------------------------|
  |-- UPLOAD_CHUNK_CONCURRENT (1) ----->|
  |<-- ACK (1) -------------------------|
  |...                                  |
  |-- UPLOAD_END --------------------->| (减少identity计数)
  |<-- OK ------------------------------|
```

**关键点**：
- 每个Socket独立发送chunk（chunk_id标识）
- Server端缓存乱序chunk，按序写入文件
- 所有Socket的UPLOAD_END都收到后，才真正关闭文件

#### 下载流程（并发请求chunk）
```
Client                                Server
  |                                      |
  |-- DOWNLOAD_START_CONCURRENT ------->| (返回文件信息)
  |<-- OK (size, total_chunks) ---------|
  |                                      |
  |-- DOWNLOAD_CHUNK_CONCURRENT (0) --->| (异步读取chunk)
  |<-- CHUNK (0, data) -----------------|
  |-- DOWNLOAD_CHUNK_CONCURRENT (1) --->|
  |<-- CHUNK (1, data) -----------------|
  |...                                  |
```

**关键点**：
- Client使用滑动窗口并发请求多个chunk
- Server异步读取文件（aiofiles），避免阻塞

## UI/UX设计原则

### 1. 进度条显示
- **简洁描述**：只显示"上传中"/"下载中"，不显示技术细节（如socket数、窗口大小）
- **固定宽度**：文件名和统计信息不应该跳动，保持稳定显示
- **实时更新粒度**：每4MB chunk更新一次，平衡性能和实时性

### 2. 完成表格布局
- **4列紧凑布局**：2对键值对并排显示，节省67%垂直空间
- **无边框设计**：使用 `show_edge=False` 和 `padding=(0, 1)` 创建清爽外观
- **关键指标**：只显示用户关心的信息（文件、大小、耗时、吞吐量），移除技术细节

### 3. list命令用户体验
- **默认聚合视图**：按顶层key分组，显示文件/目录类型、文件数、总大小
- **详细视图选项**：通过 `--detailed` 查看所有单个文件
- **符合心智模型**：用户上传什么key，就显示什么key

## 开发注意事项

### 1. 异步编程规范
- **Server端**：所有I/O操作必须使用 `aiofiles`，不能阻塞事件循环
- **Client端**：提供异步API（MultiSocketFlaxFileClient）和同步包装器（MultiSocketFlaxFileClientSync）
- **会话锁**：上传会话使用 `asyncio.Lock()` 保护并发写入的临界区

### 2. 错误处理
- ZMQ通信异常：捕获后发送 `ERROR` 帧给客户端
- 文件不存在：返回 `File not found` 错误
- 加密错误：检查密码是否一致

### 3. 性能优化
- **chunk大小**：默认4MB（平衡内存和性能）
- **ZMQ缓冲区**：RCVBUF/SNDBUF设置为128MB
- **滑动窗口**：避免网络延迟影响吞吐量
- **多Socket并发**：充分利用网络带宽

### 4. 安全考虑
- 密码通过环境变量 `FLAXFILE_PASSWORD` 传递（避免命令行泄露）
- CurveZMQ提供端到端加密
- 不信任网络必须启用加密

### 5. 调试技巧
```bash
# 启用详细日志
export PYTHONUNBUFFERED=1

# 测试加密连接
export FLAXFILE_PASSWORD="test"
flaxfile serve &
flaxfile set test.bin

# 测试多Socket传输
# 观察 server.py 日志中的 session_id 和 identity 映射
```

### 6. 常见陷阱
- **不要在锁内发送ZMQ消息**：可能导致死锁（先释放锁再发送ACK）
- **aiofiles必须用于文件I/O**：避免阻塞事件循环
- **session清理**：UPLOAD_END时需要同时清理 `upload_sessions` 和 `identity_to_session`
- **chunk乱序**：Server端必须缓存乱序chunk，按序写入文件
- **自适应策略一致性**：`calculate_adaptive_concurrency()` 计算的并发数必须与 `_auto_determine_config()` 返回的socket数匹配，否则总socket数会超出预期（参考 ADAPTIVE_STRATEGY_TEST_REPORT.md）

## 项目结构

```
flaxfile/
├── src/flaxfile/
│   ├── __init__.py           # 包入口，导出主要类
│   ├── server.py             # 异步单端口服务器
│   ├── multi_socket_client.py # 多Socket客户端
│   ├── sync.py               # 目录同步功能
│   ├── cli.py                # CLI命令入口
│   ├── config.py             # 配置管理
│   └── crypto.py             # 加密支持
├── pyproject.toml            # 项目配置和依赖
├── README.md                 # 用户文档
└── flaxfile.toml             # 配置文件示例
```

## Python API 示例

### 异步API（推荐）
```python
import asyncio
from flaxfile import MultiSocketFlaxFileClient

async def main():
    client = MultiSocketFlaxFileClient(
        server_host="127.0.0.1",
        port=25555,
        password="your_password"  # 可选
    )

    # 上传文件（自适应选择最优Socket数量）
    result = await client.upload_file("video.mp4", "my_video", show_progress=True)
    print(f"上传: {result['throughput']:.2f} MB/s")

    # 下载文件
    result = await client.download_file("my_video", "output.mp4", show_progress=True)

    # 列出文件
    files = await client.list_files(prefix="myproject/")

    # 删除文件
    await client.delete_file("my_video")

    await client.close()

asyncio.run(main())
```

### 同步API
```python
from flaxfile import MultiSocketFlaxFileClientSync

client = MultiSocketFlaxFileClientSync(server_host="127.0.0.1", port=25555)
try:
    result = client.upload_file("video.mp4", "my_video", show_progress=True)
    result = client.download_file("my_video", "output.mp4", show_progress=True)
finally:
    client.close()
```

## 配置文件格式

```toml
# flaxfile.toml

[client]
default_server = "prod"

[server]
host = "0.0.0.0"
port = 25555
storage_dir = "./zmq_streaming_storage"

[servers.local]
host = "127.0.0.1"
port = 25555

[servers.prod]
host = "192.168.1.100"
port = 25555
```

## 重要技术文档

项目中包含以下技术文档，提供了更深入的实现细节：

- **KISS_OPTIMIZATION_REPORT.md** - KISS优化原则应用和性能提升记录
- **README.md** - 用户文档和完整的功能说明

修改相关功能时应参考这些文档。

## KISS原则

本项目遵循KISS（Keep It Simple, Stupid）原则：
- **优先选择简单方案**：如依赖OS page cache而非复杂的下载会话管理
- **避免过度设计**：只在真正需要时才增加复杂性
- **代码清理**：及时删除临时测试文件和不再使用的代码
- **文档维护**：保持文档与代码同步，避免文档爆炸

## 常见开发任务

### 测试命令
```bash
# 本地测试
export FLAXFILE_PASSWORD=test
flaxfile serve &  # 启动服务器
flaxfile set test.bin  # 测试上传
flaxfile get test.bin  # 测试下载
flaxfile list  # 查看文件列表

# 清理测试数据
rm -rf ./zmq_streaming_storage
```

### 性能测试
```bash
# 创建测试文件
dd if=/dev/zero of=test_large.bin bs=1M count=1000

# 测试上传性能
time flaxfile set test_large.bin

# 测试下载性能
time flaxfile get test_large.bin output.bin
```
