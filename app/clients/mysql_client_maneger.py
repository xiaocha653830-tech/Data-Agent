"""
用来操作mysql数据库的客户端管理模块
"""
import asyncio
from typing import Optional

from sqlalchemy import text

from app.conf.app_config import DBConfig, app_config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker


class MysqlClientManger:
    def __init__(self,config:DBConfig):
        self.config = config
        self.client: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker] = None

    # 获取连接字符串
    def get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}/{self.config.database}?charset=utf8mb4"

    # 初始化
    def init_client(self):
        #创建一个异步引擎
        self.client = create_async_engine(
            self.get_url(),
            pool_size=10,
            max_overflow=5,
        )
        # 创建一个异步会话工厂
        self.session_factory = async_sessionmaker(
            self.client,
            autoflush=False,
            autobegin=True
        )

    # 释放资源
    async def close(self):
        await self.client.dispose()

dw_mysql_manager_client = MysqlClientManger(app_config.db_dw)
meta_mysql_manager_client = MysqlClientManger(app_config.db_meta)

if __name__ == '__main__':
    async def test():

        # 初始化dw客户端对象
        dw_mysql_manager_client.init_client()

        # 创建异步会话
        async with dw_mysql_manager_client.session_factory() as session:
            session: AsyncSession  # 声明类型方便后续使用

            # 执行查询sql
            sql = "select * from dim_customer limit 2"
            result = await session.execute(text(sql))

            rows = result.scalars().all()
            for row in rows:
                print(row)

        # 释放资源
        await dw_mysql_manager_client.close()

    asyncio.run(test())
        # meta_mysql_manager_client.init_client()

