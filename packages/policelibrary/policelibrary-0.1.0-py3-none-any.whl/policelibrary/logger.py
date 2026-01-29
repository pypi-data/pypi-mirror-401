import os
import sys
from pathlib import Path
from loguru import logger

# 日志文件保存路径
LOG_DIR = Path(os.getenv("POLICE_LOG_DIR", os.path.join(os.path.expanduser("~"), ".policelibrary", "logs")))
LOG_FILE = LOG_DIR / "policelibrary.log"

# 创建日志目录
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 移除默认的日志处理器
logger.remove()

# 配置日志格式
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# 添加控制台输出
logger.add(
    sys.stderr,
    format=log_format,
    level="INFO",
    colorize=True
)

# 添加文件输出
logger.add(
    str(LOG_FILE),
    format=log_format,
    level="DEBUG",  # 文件日志级别可以更详细
    rotation="10 MB",  # 日志文件大小达到 10MB 时轮转
    retention="7 days",  # 保留 7 天的日志
    compression="zip",  # 压缩旧日志
    encoding="utf-8",
    enqueue=True  # 异步写入，线程安全
)

# 导出 logger 供全局使用
__all__ = ["logger"]
