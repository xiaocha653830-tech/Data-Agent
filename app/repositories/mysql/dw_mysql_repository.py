from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

"""
用于操作mysql的dw数据库模块
"""

class DWMysqlRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_column_types(self, table_name: str) -> dict[str, str]:
        sql = f"show columns from {table_name}"
        result = await self.session.execute(text(sql))
        return {item.Field:item.Type for item in result.all()}

    async def get_column_values(self, table_name: str, column_name: str,limit: int=10) -> list:
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        return result.scalars().all()
