# 定制日志输出格式，控制输出级别
# 自动将日志内容保存到日志文件
# 指定日志文件的最大大小，一旦超过自动创建一个新的的文件
# 指定文件的有效期，过了自动删除
# 记录当前日志输出是哪个请求的，记录请求id
import sys

from loguru import logger

from app.conf.app_config import app_config
from app.core.context import get_request_id

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "  # 绿色显示日志时间（精确到毫秒）
    "<level>{level: <8}</level> | "  # 按级别颜色显示日志级别（左对齐，占8个字符）
    "<magenta>request_id - {extra[request_id]}</magenta> | "  # 品红色显示request_id（从日志extra中获取）
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "  # 青色显示日志所在文件、函数、行号
    "<level>{message}</level>"  # 按级别颜色显示日志正文
)

# 移除Loguru默认的控制台输出
logger.remove()

# 给日志打补丁
def inject_request_id(record):
    #读取请求id并保存到record
    record["extra"]["request_id"] = get_request_id()

logger = logger.patch(inject_request_id)

# 添加控制台输出的配置
if app_config.logging.console.enable:
    logger.add(
        sys.stdout,
        level=app_config.logging.console.level,
        format=log_format,
    )

if app_config.logging.file.enable:
    logger.add(
        "logs/app.log",
        level=app_config.logging.file.level,
        format=log_format,
        rotation=app_config.logging.file.rotation, #文件的最大大小
        retention=app_config.logging.file.retention,#文件的有效期
    )


if __name__ == '__main__':
    logger.trace("这是 TRACE 级别的调试信息")  # 不会输出到控制台（控制台是 INFO），但会输出到文件
    logger.debug("这是 DEBUG 级别的调试信息")  # 同上
    logger.info("服务启动成功")  # 控制台+文件都输出
    logger.success("数据同步完成")  # Loguru 独有级别
    logger.warning("内存使用率超过 80%")
    logger.error("接口调用失败：超时")
    logger.critical("数据库连接中断，服务停止")