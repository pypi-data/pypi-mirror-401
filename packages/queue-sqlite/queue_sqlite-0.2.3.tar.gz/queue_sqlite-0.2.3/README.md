# Queue SQLite - 高性能 SQLite 任务队列系统

![python-3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![rust-1.65+](https://img.shields.io/badge/rust-1.65+-red.svg)
![license-MIT](https://img.shields.io/badge/license-MIT-green.svg)
![version-0.2.1](https://img.shields.io/badge/version-0.2.1-orange.svg)


一个基于 SQLite 的高性能任务队列系统，采用 Rust 核心操作，支持任务挂载、消息监听、优先级处理、重试机制和自动清理过期消息。适合构建可靠、可扩展的后台任务处理系统。

## 🌟 特性

### 核心优势

- 🚀 高性能：Rust 核心提供毫秒级任务处理
- 💾 持久化存储：基于 SQLite 的可靠消息存储
- 🔄 多调度器支持：标准、异步、Qt 三种调度模式
- 🎯 智能分片：自动哈希分片，支持横向扩展
- 📊 全面监控：内置资源使用监控和队列状态查看

### 功能亮点

- ✅ 任务装饰器：使用 @task 装饰器轻松注册任务
- ✅ 监听装饰器：使用 @listener 装饰器实现数据变更监听
- ✅ 优先级队列：支持 LOW/NORMAL/HIGH/URGENT 四级优先级
- ✅ 重试机制：可配置的最大重试次数和延迟重试
- ✅ 过期清理：自动清理过期和完成的消息
- ✅ 批量操作：支持消息批量入队和处理
- ✅ 异步支持：原生支持 async/await 异步任务
- ✅ Qt 集成：可选 Qt 调度器用于 GUI 应用

## 📦 安装

### 前置要求

- Python 3.11+
- Rust 1.65+ (用于编译核心扩展)
- SQLite 3.35+

### 安装方式

#### 方式一：从源码安装（推荐）

```shell
# 克隆仓库
git clone https://github.com/chakcy/queue_sqlite.git
cd queue_sqlite

# 安装 Rust（如果未安装）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 Python 依赖
pip install -r requirements.txt

# 安装开发模式
pip install -e .
```

#### 方式二：从 PyPI 安装

```shell
pip install queue-sqlite
```

## 🚀 快速开始

### 基本使用

```python
from queue_sqlite.scheduler import QueueScheduler
from queue_sqlite.model import MessageItem
from queue_sqlite.constant import MessagePriority
from queue_sqlite.mounter import task


# 1. 注册任务
@task(meta={"max_retries": 3, "delay": 1})
def process_image(message_item):
    """处理图片任务"""
    data = message_item.content
    # 处理逻辑
    return {"status": "success", "processed": data["image_id"]}


# 2. 创建调度器
scheduler = QueueScheduler(scheduler_type="standard")

# 3. 启动调度器
scheduler.start()

# 4. 发送任务
for i in range(10):
    message = MessageItem(
        content={"image_id": i, "path": f"/images/{i}.jpg"},
        destination="process_image",  # 任务函数名
        priority=MessagePriority.HIGH,  # HIGH 优先级
        tags="image_processing",
    )

    def callback(result_message):
        print(f"任务完成: {result_message.id}, 结果: {result_message.result}")

    scheduler.send_message(message, callback)

# 5. 等待任务完成
import time

while scheduler.queue_operation.get_queue_length() > 0:
    print(f"剩余任务: {scheduler.queue_operation.get_queue_length()}")
    time.sleep(1)

# 6. 停止调度器
scheduler.stop()
```

### 异步任务示例

```python
import asyncio
from queue_sqlite.scheduler import QueueScheduler
from queue_sqlite.model import MessageItem
from queue_sqlite.mounter import task


@task(meta={"name": "async_processor", "max_retries": 2})
async def async_data_fetcher(message_item):
    """异步数据获取任务"""
    url = message_item.content["url"]
    # 模拟异步 HTTP 请求
    await asyncio.sleep(0.5)
    return {"url": url, "data": "fetched", "status": 200}


async def main():
    scheduler = QueueScheduler(scheduler_type="async")
    scheduler.start()

    # 发送异步任务
    message = MessageItem(
        content={"url": "https://api.example.com/data"},
        destination="async_data_fetcher",
    )

    scheduler.send_message(message, lambda m: print(f"完成: {m.id}"))

    await asyncio.sleep(5)
    scheduler.stop()


asyncio.run(main())
```

### 数据监听示例

```python
from queue_sqlite import QueueScheduler
from queue_sqlite.mounter import listener

# 注册监听器
@listener()
def user_activity_log(data):
    """监听用户活动数据"""
    print(f"用户活动: {data}")

@listener()
def system_alert(data):
    """监听系统告警"""
    print(f"系统告警: {data}")

# 创建调度器
scheduler = QueueScheduler()
scheduler.start()

# 更新监听数据（会自动触发监听函数）
scheduler.update_listen_data("user_activity_log", "用户登录")
scheduler.update_listen_data("user_activity_log", "用户购买")
scheduler.update_listen_data("system_alert", "CPU使用率过高")
```

## ⚙️ 配置选项

### 调度器配置

```python
from queue_sqlite import SchedulerConfig, QueueScheduler

config = SchedulerConfig(
    receive_thread_num=2,    # 接收线程数
    task_thread_num=8,       # 任务执行线程数
    shard_num=4,             # 数据库分片数
    queue_name="production", # 队列名称
    meta={"app": "myapp"}    # 自定义元数据
)

scheduler = QueueScheduler(
    scheduler_type="standard",  # standard | async | qt
    config=config
)
```

### 消息配置

```python
from queue_sqlite import MessageItem
from queue_sqlite.constant import MessagePriority, MessageType
from datetime import datetime, timedelta

message = MessageItem(
    # 必需字段
    content={"data": "任务数据"},
    destination="task_function_name",
    
    # 可选字段
    id="custom-uuid",  # 默认自动生成
    type=MessageType.TASK,
    priority=MessagePriority.HIGH,
    source="web_api",
    tags="urgent,processing",
    
    # 时间控制
    expire_time=datetime.now() + timedelta(hours=1),  # 1小时后过期
    retry_count=0,
    
    # 自定义元数据
    metadata={"user_id": 123, "request_id": "abc123"}
)
```

## 📊 系统架构

### 架构图

```text
┌─────────────────────────────────────────────────────────┐
│                    Python application                   |
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────┐   │
│  │   @task     │  │ @listener   │  │ QueueScheduler │   │
│  │             │  │             │  │                │   │
│  └─────────────┘  └─────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  Python Service                         │
│  ┌──────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ TaskMounter  │  │ TaskCycle   │  │ Schedulers  │     │
│  │ ListenMounter│  │ AsyncCycle  │  │             │     │
│  └──────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Rust core                             │
│  ┌─────────────────────────────────────────┐            │
│  │      queue_sqlite_core                  │            │
│  │  • shared sqlite database               │            │
│  │  • SQLite Optimization                  │            │
│  │  • Connection pool                      │            │
│  └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  SQLite database                        │
│  ┌───────────────────────────────────────────────┐      │
│  │      shared database (cache/queue_name/)      │      │
│  │  • queue_shard_0.db                           │      │
│  │  • queue_shard_1.db                           │      │
│  │  • listen.db                                  │      │
│  └───────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 组件说明

1. **MessageIte**: 核心数据模型，包含消息的所有属性和方法
2. **TaskMounter**: 任务过载器，通过装饰器注册任务函数
3. **ListenMounter**：监听挂载器，通过装饰器注册监听函数
4. **TaskCycle**：任务生命周期管理器，处理重试和状态更新
5. **QueueScheduler**：统一调度器接口，支持三种实现：
   - **StandardQueueScheduler**：统一调度器接口，支持三种实现：
   - **AsyncQueueScheduler**：异步/等待实现
   - **QtQueueScheduler**：Qt 线程池实现（GUI应用）
6. **CleanupScheduler**：自动清理过期消息
7. **ShardedQueueOperation**：Rust 实现的高性能分片队列操作

## 🧪 测试

### 运行测试套件

```bash
# 运行所有测试
python -m -v -s pytest tests/

# 运行特定测试
python -m pytest tests/test_stress.py -v
python -m pytest tests/test_async_scheduler.py -v
```

### 性能测试示例

```python
from tests.test_stress import TestStress

# 压力测试：处理 10000 个任务
TestStress.test_stress()

# 异步调度器测试
from tests.test_async_scheduler import TestAsyncScheduler
TestAsyncScheduler.test_async_scheduler()
```

## 📈 性能指标

### 基准测试结果

| 指标 | 标准调度器 | 异步调度器 | Qt 调度器 |
| --- | ---------- | ---------- | --------- |
| 单核 QPS | 5,000+ | 8,000+ | 6,000+ |
| 内存占用 | 50-100MB | 60-120MB | 70-150MB |
| 延迟（p95） | <50ms | <30ms | <40ms |
| 最大并发 | 1,000+ | 2,000+ | 1500+ |

### 扩展性测试

- 10 分片：支持 50,000+ 并发任务
- 自动负载均衡：分片间任务均匀分布
- 线性扩展：增加分片数可线性提升吞吐量

## 📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

## 📞 联系与支持

- **作者**: chakcy
- **邮箱**: 947105045@qq.com

## 🙏 致谢

感谢以下开源项目：

- [SQLite](https://www.sqlite.org/) - 轻量级嵌入式数据库
- [PyO3](https://pyo3.rs/) - Rust-Python 绑定
- [r2d2](https://github.com/sfackler/r2d2) - Rust 数据库连接池

---

**Queue SQLite** - 为您的应用提供可靠、高效的任务队列解决方案。
