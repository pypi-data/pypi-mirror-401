# MinLog

一个简洁的Python日志工具包，提供彩色控制台输出、文件日志记录和美观的日志框功能。

## 功能特性

- `setup_logging()`: 初始化日志系统，自动创建`logs`目录，将日志输出到控制台和文件
- `get_logger(name)`: 获取指定名称的logger实例
- `log_box(logger, title, data)`: 以框线形式美化输出复杂数据
+
+### 结构化日志功能（类似structlog）
+- `get_structured_logger(name)`: 获取支持结构化日志的记录器
+- `bind_global(**kwargs)`: 绑定全局上下文信息
+- `unbind_global(*keys)`: 移除全局上下文键
+- `add_processor(processor)`: 添加自定义处理器
+- 支持位置参数绑定：`logger.bind("Request Info", request_id="req-001")`
+- 异常处理：自动捕获并格式化异常信息
+- 可切换渲染器：支持JSON和键值对等多种输出格式
+- **交互式全景日志 (Log-as-an-App)**: 生成单文件、交互式的 HTML 报表，支持时间轴和附件预览
- **并发支持**: 基于 `contextvars` 实现多线程和 `asyncio` 任务间的上下文隔离
- **安全脱敏**: 内置 `RedactingProcessor` 自动屏蔽敏感数据（如 password/token）
- **动态配置**: 支持配置文件热重载，无需重启即可调整日志级别
- **极致性能**: 实现了日志等级预检查 (Level Pre-check)，未启用的日志级别几乎零性能损耗
- **配置与轮放**: 支持 `config.json` 配置文件和自动日志轮放


## 配置说明

项目支持通过根目录下的 `config.json` 进行配置：

```json
{
  "log_dir": "logs",
  "log_level": "DEBUG",
  "rotation": {
    "max_bytes": 10485760,
    "backup_count": 5
  },
  "enable_color": true
}
```

- `log_dir`: 日志保存目录
- `log_level`: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `rotation`: 日志轮放配置 (`max_bytes` 为单个文件最大字节数，`backup_count` 为保留的旧日志数量)
- `enable_color`: 是否启用控制台彩色输出

## 快速开始


```python
from MinLog import setup_logging, get_logger, log_box

# 1. 初始化日志系统
setup_logging()

# 2. 获取logger
logger = get_logger("MyComponent")

# 3. 使用日志框输出数据
data = {
    "Key 1": "Value 1",
    "Key 2": "A very long value that should wrap because it exceeds the terminal width potentially or just the box limit."
}
log_box(logger, "Test Box", data)
```

### 结构化日志示例

```python
from MinLog import setup_logging, get_structured_logger, bind_global, add_processor
import json

# 初始化
setup_logging()

# 添加时间戳处理器
def add_timestamp(logger, method_name, event_dict):
    from datetime import datetime
    event_dict['timestamp'] = datetime.now().isoformat()
    return event_dict
add_processor(add_timestamp)

# 绑定全局上下文
bind_global(service="MyService")

# 使用结构化日志
logger = get_structured_logger("StructuredComponent")
logger.info("user_login", user_id=123, ip="192.168.1.1")
```

日志文件将保存在项目根目录下的`logs`文件夹中。