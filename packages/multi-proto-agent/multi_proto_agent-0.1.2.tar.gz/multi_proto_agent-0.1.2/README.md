# Multi-Proto-Agent

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 项目简介

**Multi-Proto-Agent** 是一个强大的多协议通信框架，旨在简化基于多种协议的消息通信。框架内置了对 **JSON** 和 **Protobuf** 的序列化、反序列化支持，并设计为**线程安全**，让你可以轻松创建和管理**成百上千个并发通信代理**。

### 核心特性

- 🔌 **多协议支持**：支持 TCP 和 WebSocket（WS/WSS）协议
- 📦 **序列化支持**：内置 JSON 和 Protobuf 序列化/反序列化
- 🔒 **线程安全**：所有组件设计为线程安全，支持高并发场景
- 🚀 **高并发管理**：轻松创建和管理数百个并发通信代理
- 💓 **心跳机制**：内置自动心跳保活机制，确保连接稳定性
- 📊 **消息队列**：基于队列的消息接收机制，支持异步处理
- 🛠️ **工具完备**：提供协议生成工具、配置管理、日志系统等
- 📝 **完整日志**：统一的日志配置，支持文件和控制台输出

## 🚀 快速开始

### 安装

#### 方式一：使用 pip 安装

```bash
pip install multi-proto-agent
```

#### 方式二：从源码安装

```bash
git clone https://gitee.com/flinttina/multi-proto-agent.git
cd multi-proto-agent
pip install -e .
```

### 依赖要求

- Python >= 3.8
- 主要依赖：
  - `protobuf >= 5.28.3`
  - `websocket-client >= 1.9.0`
  - `PyYAML >= 6.0.2`
  - `gevent >= 25.9.1`

完整依赖列表请查看 [requirements.txt](requirements.txt)

## 📚 使用示例

### 基础示例：创建单个通信代理

```python
from utils.player import Player
from python_protos.share import Base_pb2

# 创建玩家/代理实例
player = Player(
    account_id="player_001",
    role_name="测试角色",
    protocol_type="ws"  # 或 "tcp"
)

# 设置连接信息
player.set_ap_address("ws://192.168.1.100:8080")
player.set_secret_key("your_secret_key")

# 建立连接
try:
    player.connect()
    print("连接成功！")
    
    # 发送请求
    req_obj = Base_pb2.ReqHeartbeat()
    player.send_request("Base.ReqHeartbeat", req_obj)
    
    # 接收响应
    response = player.receive_response()
    if response:
        print(f"收到响应: {response}")
    
except ConnectionError as e:
    print(f"连接失败: {e}")
finally:
    # 清理资源
    player.tear_down()
```

### 高级示例：管理多个并发代理

```python
import threading
from utils.player import Player
from utils.config_util import set_config

# 设置环境配置
set_config("test_env", config_path="./test_configurations/env_config.yaml")

# 创建多个代理
players = []
for i in range(100):
    player = Player(
        account_id=f"player_{i:03d}",
        protocol_type="ws"
    )
    player.set_ap_address("ws://192.168.1.100:8080")
    player.set_secret_key("your_secret_key")
    players.append(player)

# 并发连接
def connect_player(player):
    try:
        player.connect()
        print(f"{player.account_id} 连接成功")
    except Exception as e:
        print(f"{player.account_id} 连接失败: {e}")

# 使用线程池并发连接
threads = []
for player in players:
    thread = threading.Thread(target=connect_player, args=(player,))
    thread.start()
    threads.append(thread)

# 等待所有连接完成
for thread in threads:
    thread.join()

# 批量发送请求
for player in players:
    if player.player_client and player.player_client.is_connected:
        req_obj = Base_pb2.ReqHeartbeat()
        player.send_request("Base.ReqHeartbeat", req_obj)

# 清理所有资源
for player in players:
    player.tear_down()
```

### TCP 协议示例

```python
from utils.tcp_util import TcpClient

# 创建 TCP 客户端
tcp_client = TcpClient(length_prefix_bytes=2)

# 连接服务器
if tcp_client.connect(("192.168.1.100", 8080), account_id="tcp_client_001"):
    # 发送数据
    data = b"Hello, TCP Server!"
    tcp_client.send(data)
    
    # 接收数据（从队列获取）
    if tcp_client.queue_size() > 0:
        response = tcp_client.message_queue.get()
        print(f"收到响应: {response}")
    
    # 关闭连接
    tcp_client.close()
```

### WebSocket 协议示例

```python
from utils.websocket_util import WebSocketClient

# 创建 WebSocket 客户端
ws_client = WebSocketClient(
    length_prefix_bytes=2,
    account_id="ws_client_001"
)

# 连接服务器
try:
    ws_client.connect("ws://192.168.1.100:8080", secret_key="your_key")
    
    # 发送消息
    message = b"Hello, WebSocket Server!"
    ws_client.send(message)
    
    # 接收消息（从队列获取）
    if ws_client.message_queue.qsize() > 0:
        response = ws_client.message_queue.get()
        print(f"收到响应: {response}")
    
except ConnectionError as e:
    print(f"连接失败: {e}")
finally:
    ws_client.close()
```

## 🏗️ 项目结构

```
multi-proto-agent/
├── utils/                  # 核心工具模块
│   ├── player.py          # Player 类：通信代理封装
│   ├── tcp_util.py        # TCP 客户端工具
│   ├── websocket_util.py   # WebSocket 客户端工具
│   ├── translator.py      # 序列化/反序列化工具
│   ├── config_util.py     # 配置管理工具
│   ├── logger_config.py   # 日志配置
│   └── ...                # 其他工具模块
├── tools/                 # 工具脚本
│   ├── gen_pb2_py.py      # Protobuf 代码生成工具
│   └── protoc.exe         # Protobuf 编译器
├── python_protos/         # 生成的 Protobuf Python 代码
├── proto/                 # Protobuf 定义文件
├── setup.py               # 安装配置
├── requirements.txt       # 依赖列表
└── README.md             # 项目文档
```

## 🔧 配置说明

### 环境变量配置

框架支持通过环境变量进行配置：

```python
import os
from utils.config_util import set_config

# 设置环境配置
set_config("test_env", config_path="./test_configurations/env_config.yaml")

# 或直接设置环境变量
os.environ['heartbeat_interval'] = '30'  # 心跳间隔（秒）
os.environ['tcp_length_prefix_bytes'] = '2'  # TCP 长度前缀字节数
os.environ['ws_length_prefix_bytes'] = '2'   # WebSocket 长度前缀字节数
os.environ['LOG_LEVEL'] = 'INFO'  # 日志级别
```

### Protobuf 配置

使用 `gen_pb2_py.py` 工具生成 Protobuf Python 代码：

```bash
python tools/gen_pb2_py.py
```

该工具会：
1. 从 `proto/` 目录读取 `.proto` 文件
2. 生成 Python 代码到 `python_protos/` 目录
3. 自动修复导入语句
4. 生成配置文件 `test_configurations/protos_config.yaml`

## 📖 API 文档

### Player 类

`Player` 类是框架的核心，封装了完整的通信代理功能。

#### 初始化

```python
player = Player(
    account_id="player_001",      # 账号ID（必需）
    role_name="角色名",             # 角色名称（可选）
    role_uid="uid_001",            # 角色UID（可选）
    protocol_type="ws"             # 协议类型：'tcp', 'ws', 'wss'
)
```

#### 主要方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `connect(max_retry_times=3)` | 建立连接，支持自动重试 | `bool` |
| `send_request(req_msg_name, req_obj, is_heartbeat=False)` | 发送请求消息 | `bool` |
| `receive_response()` | 接收响应消息 | `bytes` 或 `None` |
| `tear_down()` | 清理资源，关闭连接 | `None` |
| `set_ap_address(address)` | 设置服务器地址 | `None` |
| `set_secret_key(key)` | 设置连接密钥 | `None` |

#### 属性访问器

Player 类提供了完整的 getter/setter 方法：

```python
# 账号相关
player.get_account_id()
player.set_account_id("new_id")

# 角色相关
player.get_role_name()
player.set_role_name("新角色名")
player.get_role_uid()
player.set_role_uid("new_uid")

# 连接相关
player.get_ap_address()
player.set_ap_address("ws://192.168.1.100:8080")
player.get_secret_key()
player.set_secret_key("secret")

# 协议相关
player.get_protocol_type()
player.set_protocol_type("tcp")
```

### TcpClient 类

TCP 客户端封装类。

```python
from utils.tcp_util import TcpClient

tcp_client = TcpClient(length_prefix_bytes=2)
tcp_client.connect(("ip", port), timeout=5, account_id="client_001")
tcp_client.send(data)
response = tcp_client.message_queue.get()
tcp_client.close()
```

### WebSocketClient 类

WebSocket 客户端封装类。

```python
from utils.websocket_util import WebSocketClient

ws_client = WebSocketClient(length_prefix_bytes=2, account_id="ws_001")
ws_client.connect("ws://host:port", secret_key="key")
ws_client.send(message_bytes)
response = ws_client.message_queue.get()
ws_client.close()
```

### Translator 工具

序列化/反序列化工具。

```python
from utils.translator import handle_send_data, handle_rsp_data

# 序列化发送数据
req_data = handle_send_data("Base.ReqHeartbeat", req_obj, trace_id="trace_001")

# 反序列化响应数据
rsp_msg = handle_rsp_data(rsp_data)
# 返回格式: {"Base.RspHeartbeat": "{...}", "trace_id": "trace_001"}
```

## 🎯 使用场景

- **游戏服务器压力测试**：模拟大量玩家并发连接
- **消息推送系统**：管理大量 WebSocket 连接
- **IoT 设备管理**：管理大量设备的 TCP/WebSocket 连接
- **API 测试框架**：自动化测试多协议接口
- **实时通信系统**：构建高并发的实时通信应用

## 🔍 特性详解

### 线程安全设计

- 所有客户端类使用线程安全的队列（`queue.Queue`）
- 使用 `threading.Event` 进行线程同步
- 连接状态检查使用线程安全标志

### 心跳机制

Player 类内置心跳机制，自动维护连接：

```python
# 设置心跳间隔（秒）
os.environ['heartbeat_interval'] = '30'

# Player 连接后自动启动心跳线程
player.connect()
# 心跳线程会自动发送心跳包，失败3次后自动断开连接
```

### 消息队列

所有消息通过队列接收，支持异步处理：

```python
# 检查队列大小
size = player.rsp_queue.qsize()

# 非阻塞获取消息
try:
    message = player.rsp_queue.get(block=False)
except queue.Empty:
    # 队列为空
    pass

# 阻塞获取消息（带超时）
message = player.rsp_queue.get(timeout=5)
```

### 长度前缀支持

支持自定义长度前缀字节数（0、2、4字节）：

```python
# TCP: 2字节长度前缀
tcp_client = TcpClient(length_prefix_bytes=2)

# WebSocket: 4字节长度前缀
ws_client = WebSocketClient(length_prefix_bytes=4)

# 无长度前缀
ws_client = WebSocketClient(length_prefix_bytes=0)
```

## 🛠️ 开发指南

### 生成 Protobuf 代码

1. 将 `.proto` 文件放入 `proto/` 目录
2. 运行生成脚本：

```bash
python tools/gen_pb2_py.py
```

3. 生成的 Python 代码位于 `python_protos/` 目录

### 添加新的协议支持

框架设计为可扩展，可以轻松添加新的协议支持：

1. 在 `utils/` 目录创建新的客户端类
2. 实现与 `TcpClient` 和 `WebSocketClient` 类似的接口
3. 在 `Player` 类中添加协议类型支持

### 日志配置

```python
from utils.logger_config import setup_logging, get_logger

# 配置日志
setup_logging(level=logging.INFO, log_dir="./logs")

# 获取 logger
logger = get_logger(__name__)
logger.info("这是一条日志")
```

## 📝 注意事项

1. **资源清理**：使用完 Player 实例后，务必调用 `tear_down()` 方法清理资源
2. **线程安全**：虽然框架是线程安全的，但在多线程环境中使用时要确保正确同步
3. **连接管理**：大量并发连接时，注意系统资源限制（文件描述符、内存等）
4. **错误处理**：建议使用 try-except 捕获连接和发送异常
5. **心跳配置**：根据实际需求调整心跳间隔，避免过于频繁

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👤 作者

**Shi Feng**

- Email: 330550850@qq.com
- Gitee: [@flinttina](https://gitee.com/flinttina)

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
