import atexit
import copy
import json
import logging
import os
import queue
import sys
import threading
import time
import traceback
from contextvars import ContextVar
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

LOG_COLORS = {
    "DEBUG": "\033[36m",  # 青色
    "INFO": "\033[32m",  # 绿色
    "WARNING": "\033[33m",  # 黄色
    "ERROR": "\033[31m",  # 红色
    "CRITICAL": "\033[41m",  # 红底
}
RESET = "\033[0m"
DYNASCRIPT_COLOR = "\033[1;35m"  # 修正拼写错误并统一命名风格


def _should_color():
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%", enable_color=True):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.enable_color = enable_color

    def format(self, record):
        rec = copy.copy(record)

        if self.enable_color:
            level_text = rec.levelname
            level_color = LOG_COLORS.get(level_text, "")
            if level_color:
                level_colored = f"{level_color}{level_text}{RESET}"
                rec.levelname = level_colored

        message = super().format(rec)

        if self.enable_color:
            message = message.replace("[MinLog]", f"{DYNASCRIPT_COLOR}[MinLog]{RESET}")
        return message


DEFAULT_CONFIG = {
    "log_dir": "logs",
    "log_level": "DEBUG",
    "rotation": {
        "max_bytes": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5,
    },
    "enable_color": True,
}


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """从配置文件加载配置，如果失败则返回默认配置"""
    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
    except Exception as e:
        print(f"[MinLog] WARN: Failed to load config from {config_path}: {e}", file=sys.stderr)
    return DEFAULT_CONFIG


def setup_logging():
    for h in logging.root.handlers[:]:
        logging.root.removeHandler(h)

    config = load_config()

    log_dir = Path(config["log_dir"])
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[MinLog] WARN: cannot create log dir: {e}", file=sys.stderr)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    project_name = Path(os.getcwd()).name
    log_path = log_dir / f"{timestamp}_{project_name}.log"

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    enable_color = config.get("enable_color", _should_color())
    console_formatter = ColorFormatter("[MinLog][%(levelname)-8s] %(message)s", enable_color=enable_color)
    console_handler.setFormatter(console_formatter)

    log_level = getattr(logging, config["log_level"].upper(), logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    # File handler (with rotation)
    try:
        rotation_cfg = config.get("rotation", DEFAULT_CONFIG["rotation"])
        file_handler = RotatingFileHandler(
            filename=log_path,
            encoding="utf-8",
            maxBytes=rotation_cfg.get("max_bytes", DEFAULT_CONFIG["rotation"]["max_bytes"]),
            backupCount=rotation_cfg.get("backup_count", DEFAULT_CONFIG["rotation"]["backup_count"]),
        )
    except Exception as e:
        print(f"[MinLog] ERROR: cannot open log file: {e}", file=sys.stderr)
        file_handler = None

    file_formatter = logging.Formatter(
        fmt="[%(levelname)-8s][%(asctime)s.%(msecs)03d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    if file_handler:
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)

        # Wrap with AsyncHandler if configured
        if config.get("async", False):
            file_handler = AsyncHandler(file_handler)

    handlers = [console_handler] + ([file_handler] if file_handler else [])

    logging.basicConfig(level=log_level, handlers=handlers, force=True)

    if config.get("hot_reload", False):
        start_hot_reload_monitor(log_path)


_hot_reload_thread = None


def start_hot_reload_monitor(log_path):
    global _hot_reload_thread
    if _hot_reload_thread and _hot_reload_thread.is_alive():
        return

    def monitor():
        last_mtime = 0
        config_path = "config.json"
        while True:
            try:
                if os.path.exists(config_path):
                    mtime = os.path.getmtime(config_path)
                    if last_mtime != 0 and mtime > last_mtime:
                        print("[MinLog] Config changed, reloading...", file=sys.stdout)
                        # 这里简单粗暴地重新调用 setup_logging
                        # 注意：在生产环境中可能需要更精细的重新配置，而不是完全重置
                        # 但对于当前架构，setup_logging 具有幂等性和清理能力 (removeHandler)
                        # 需要小心死循环调用，但 setup_logging 中只有 config["hot_reload"] 为 True 时才启动 monitor
                        # 因此我们需要避免 monitor 再次被启动

                        # 重新加载配置并更新 Logger Adapter
                        new_config = load_config()
                        new_level_name = new_config.get("log_level", "DEBUG").upper()
                        new_level = getattr(logging, new_level_name, logging.DEBUG)

                        root = logging.getLogger()
                        root.setLevel(new_level)
                        for h in root.handlers:
                            h.setLevel(new_level)

                    last_mtime = mtime
            except Exception:
                pass
            time.sleep(3)  # Check every 3 seconds

    _hot_reload_thread = threading.Thread(target=monitor, daemon=True)
    _hot_reload_thread.start()

    # logging.debug("Logging initialized (level=%s, file=%s)", str(log_path))


class BoundLogger:
    """优化版结构化日志绑定器，支持上下文链和异常处理"""

    def __init__(self, logger: logging.Logger, *args, **context):
        self.logger = logger
        self._context = self._process_args(args, context)
        self._parent = None

    def _process_args(self, args: Tuple, kwargs: Dict) -> Dict:
        """处理位置参数和关键字参数"""
        if len(args) == 1 and isinstance(args[0], dict):
            return {**args[0], **kwargs}
        elif args:
            return {"event": " ".join(map(str, args)), **kwargs}
        return kwargs

    def bind(self, *args, **new_values) -> "BoundLogger":
        """绑定新上下文，支持位置参数"""
        new_ctx = self._process_args(args, new_values)
        child = BoundLogger(self.logger, **new_ctx)
        child._parent = self
        return child

    def unbind(self, *keys) -> "BoundLogger":
        """移除指定上下文键"""
        new_ctx = {k: v for k, v in self._context.items() if k not in keys}
        return self.bind(**new_ctx)

    def new(self, *args, **new_values) -> "BoundLogger":
        """创建全新上下文"""
        return BoundLogger(self.logger, *args, **new_values)

    @property
    def full_context(self) -> Dict[str, Any]:
        """获取完整上下文（避免深拷贝）"""
        if self._parent is None:
            return self._context
        parent_ctx = self._parent.full_context
        return {**parent_ctx, **self._context}

    def _format_exception(self, exc_info: Tuple) -> Dict:
        """格式化异常信息"""
        exc_type, exc_value, tb = exc_info
        return {"exception": {"type": exc_type.__name__, "value": str(exc_value), "traceback": traceback.format_tb(tb)}}

    def _process_event(self, event: str, **kw) -> Dict:
        """处理结构化日志事件"""
        event_dict = {**self.full_context, **kw}
        event_dict["event"] = event
        return event_dict

    def info(self, event: str, *args, **kw):
        self._log(logging.INFO, event, *args, **kw)

    def debug(self, event: str, *args, **kw):
        self._log(logging.DEBUG, event, *args, **kw)

    def warning(self, event: str, *args, **kw):
        self._log(logging.WARNING, event, *args, **kw)

    def error(self, event: str, *args, **kw):
        exc_info = sys.exc_info()
        if exc_info[0] is not None:
            kw.update(self._format_exception(exc_info))
        self._log(logging.ERROR, event, *args, **kw)

    def critical(self, event: str, *args, **kw):
        self._log(logging.CRITICAL, event, *args, **kw)

    def _log(self, level: int, event: str, *args, **kw):
        """核心日志处理方法"""
        # [优化] 性能预检查：如果不满足日志级别，直接跳过所有处理
        if not self.logger.isEnabledFor(level):
            return

        event_dict = self._process_event(event, *args, **kw)
        # 处理器链返回的是最终要渲染的字符串
        processed = _processor_chain.process(self.logger, logging.getLevelName(level), event_dict)
        self.logger.log(level, processed)


class RedactingProcessor:
    """敏感数据脱敏处理器"""

    def __init__(self, sensitive_keys: List[str] = None):
        self.sensitive_keys = sensitive_keys or ["password", "secret", "token", "auth", "key"]

    def __call__(self, logger, method_name, event_dict):
        for key in self.sensitive_keys:
            if key in event_dict:
                event_dict[key] = "***HIDDEN***"
        return event_dict


class ProcessorChain:
    """日志处理器链，类似structlog的处理器链"""

    def __init__(self, processors: List[Callable] = None):
        self.processors = processors or []

    def process(self, logger: logging.Logger, method_name: str, event_dict: Dict) -> str:
        """处理事件字典，返回最终要输出的字符串"""
        current = event_dict
        for processor in self.processors:
            try:
                result = processor(logger, method_name, current)
                # 如果处理器返回的是字符串，说明已经渲染完成
                if isinstance(result, str):
                    return result
                current = result
            except Exception as e:
                # 安全回退，避免日志系统崩溃
                fallback = {
                    "event": "log_processor_failed",
                    "processor": getattr(processor, "__name__", "unknown"),
                    "error": str(e),
                    "original_event": event_dict,
                }
                return json.dumps(fallback, ensure_ascii=False)
        # 最终使用全局渲染器
        return _renderer(current)

    def add(self, processor: Callable):
        self.processors.append(processor)


class AsyncHandler(logging.Handler):
    """
    Asynchronous logging handler using a background thread and a queue.
    Ensures that the main application thread is not blocked by slow I/O.
    """

    def __init__(self, target_handler: logging.Handler, max_queue_size: int = 10000):
        super().__init__()
        self.target_handler = target_handler
        self.queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True, name="MinLog-AsyncWorker")
        self._thread.start()
        atexit.register(self.shutdown)

    def emit(self, record):
        try:
            if not self._stop_event.is_set():
                self.queue.put_nowait(record)
        except queue.Full:
            sys.stderr.write("[MinLog] Async queue full, dropping log record\n")
        except Exception:
            self.handleError(record)

    def _worker(self):
        while not self._stop_event.is_set() or not self.queue.empty():
            try:
                record = self.queue.get(timeout=0.1)
                self.target_handler.emit(record)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                sys.stderr.write("[MinLog] Error in async worker\n")

    def shutdown(self):
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings for Observability.
    Compatible with ECS/Filebeat/Fluentd.
    """

    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "func": record.funcName,
            "lineno": record.lineno,
            "process": record.process,
            "thread": record.threadName,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


_processor_chain = ProcessorChain()

_global_context: ContextVar[Dict[str, Any]] = ContextVar("global_context", default={})


def get_structured_logger(name: str) -> BoundLogger:
    """获取结构化日志记录器"""
    logger = logging.getLogger(name)
    current_ctx = _global_context.get()
    return BoundLogger(logger, **current_ctx.copy())


def bind_global(*args, **new_values):
    """绑定全局上下文 (按线程/协程隔离)"""
    current_ctx = _global_context.get()
    new_ctx = BoundLogger(None, *args, **new_values).full_context
    _global_context.set({**current_ctx, **new_ctx})


def unbind_global(*keys):
    """移除全局上下文键 (按线程/协程隔离)"""
    current_ctx = _global_context.get()
    new_ctx = {k: v for k, v in current_ctx.items() if k not in keys}
    _global_context.set(new_ctx)


def add_processor(processor: Callable):
    """添加日志处理器"""
    _processor_chain.add(processor)


# 默认添加异常处理器
def format_exc_info(logger, method_name, event_dict):
    """格式化异常信息处理器"""
    if "exception" in event_dict:
        exc = event_dict["exception"]
        event_dict["exception_info"] = {
            "type": exc["type"],
            "value": exc["value"],
            "traceback": "\n".join(exc["traceback"]),
        }
        del event_dict["exception"]
    return event_dict


add_processor(format_exc_info)
# 默认添加脱敏处理器
add_processor(RedactingProcessor())


# 添加键值对格式化器
def key_value_renderer(logger, method_name, event_dict):
    """键值对格式化器"""
    parts = [f"[{method_name.upper()}] {event_dict.pop('event', '')}"]
    for key, value in event_dict.items():
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)
        parts.append(f"{key}={value}")
    return " ".join(parts)


# 可通过 set_renderer 切换渲染器
_renderer = json.dumps


def set_renderer(renderer: Callable[[Dict], str]):
    """设置日志渲染器"""
    global _renderer
    _renderer = renderer


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取标准 Logger 实例"""
    if name:
        return logging.getLogger(f"MinLog.{name}")
    return logging.getLogger("MinLog")
