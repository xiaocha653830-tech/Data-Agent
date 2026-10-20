from qdrant_client import AsyncQdrantClient

"""
用于操作qdrant数据库中字段信息的持久层模块
"""

class ColumnQdrantRepository:
    def __init__(self,client: AsyncQdrantClient):
        self.client = client