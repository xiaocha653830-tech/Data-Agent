from langgraph.runtime import Runtime

from app.agent.context import DateAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def generate_sql(state: DataAgentState, runtime: Runtime[DateAgentContext]):
    # 自定义数据输出
    runtime.stream_writer("生成SQL")

    try:
        # 处理
        return {}
    except Exception as e:
        logger.error(f"生成SQL失败：{str(e)}")
        raise