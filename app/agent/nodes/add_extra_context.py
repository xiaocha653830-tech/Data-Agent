from langgraph.runtime import Runtime

from app.agent.context import DateAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def add_extra_context(state: DataAgentState, runtime: Runtime[DateAgentContext]):
    # 自定义数据输出
    runtime.stream_writer("添加额外信息")

    try:
        # 处理
        return {}
    except Exception as e:
        logger.error(f"添加额外信息失败：{str(e)}")
        raise