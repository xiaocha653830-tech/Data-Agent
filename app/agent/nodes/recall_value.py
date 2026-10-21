from langgraph.runtime import Runtime

from app.agent.context import DateAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def recall_value(state: DataAgentState, runtime: Runtime[DateAgentContext]):
    # 自定义数据输出
    runtime.stream_writer("召回字段值")

    try:
        # 处理
        return {}
    except Exception as e:
        logger.error(f"召回字段值失败：{str(e)}")
        raise