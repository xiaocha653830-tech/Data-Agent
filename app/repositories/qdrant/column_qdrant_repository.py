import random

from qdrant_client import AsyncQdrantClient, models
from app.conf.app_config import app_config
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant

"""
用于操作qdrant数据库中字段信息的持久层模块
"""

class ColumnQdrantRepository:
    collection_name = "data-agent-column_collection2"
    def __init__(self,client: AsyncQdrantClient):
        self.client = client

    async def _create_collection(self):
        client = self.client
        collection_name = self.collection_name

        if await client.collection_exists(collection_name=collection_name):
            await client.delete_collection(collection_name=collection_name)
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size = app_config.qdrant.embedding_size,
                distance=models.Distance.COSINE
            )
        )


    #批量保存多个字段信息的向量列表
    async def insert_column_vectors(self, ids:list[str], payloads:list[ColumnInfoQdrant], vectors: list[list[float]]):
        print(f"🔥 Qdrant 接收到的数据总数: {len(ids)} 条")  # 加在这里！
        await self._create_collection()

        batch_size = 20
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            print(f"🚀 正在插入批次: {i} 到 {i + len(batch_ids)}，本批数量: {len(batch_ids)}")  # 加在这里！
            batch_payloads = payloads[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]

            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=batch_ids[i],
                        payload=batch_payloads[i],
                        vector=batch_vectors[i],
                    )
                    for i in range(len(batch_ids))
                ],
            )