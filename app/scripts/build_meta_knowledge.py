import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import logger

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_maneger import dw_mysql_manager_client, meta_mysql_manager_client
from app.clients.qdrant_client_manager import qdrant_client_manager


from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw_mysql_repository import DWMysqlRepository
from app.repositories.mysql.meta_mysql_repository import MetaMysqlRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository

from app.services.meta_knowledge_service import MetaKnowledgeService

"""
构建元数据知识库入库脚本文件
1. 初始化客户端
2. 创建业务层对象（先创建会话，持久层对象）
3. 调用构建的业务方法进行构建处理
4. 成功了提交事务，失败了回滚事务
5. 无论成功失败，都要关闭客户端
"""

async def start_build():

    logger.info("启动元数据知识库构建")

    embedding_client_manager.init_client()
    qdrant_client_manager.init_client()
    es_client_manager.init_client()
    dw_mysql_manager_client.init_client()
    meta_mysql_manager_client.init_client()

    try:
        assert dw_mysql_manager_client.session_factory
        async with (
            dw_mysql_manager_client.session_factory() as dw_session,
            meta_mysql_manager_client.session_factory() as meta_session,
        ):
            meta_session: AsyncSession
            service = MetaKnowledgeService(
                dw_mysql_repo=DWMysqlRepository(dw_session),
                meta_mysql_repo=MetaMysqlRepository(meta_session),
                value_es_repo=ValueESRepository(es_client_manager.client),
                column_qdrant_repo=ColumnQdrantRepository(qdrant_client_manager.client),
                metric_qdrant_repo=MetricQdrantRepository(qdrant_client_manager.client),
                embedding_client=embedding_client_manager.client
            )
            await service.build()

            await meta_session.commit()
            logger.info("构建知识库成功")

    except Exception as e:
        logger.error(f"构建元知识库失败", {str(e)})
        await meta_session.rollback()

        raise
    finally:
        await dw_mysql_manager_client.close()
        await meta_mysql_manager_client.close()
        await qdrant_client_manager.close()
        await es_client_manager.close()

if __name__ == '__main__':
    asyncio.run(start_build())