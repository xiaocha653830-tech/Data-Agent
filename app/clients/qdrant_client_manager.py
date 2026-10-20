import random
from typing import Optional

from qdrant_client import AsyncQdrantClient, models
import asyncio

from app.conf.app_config import app_config
from app.conf.app_config import QdrantConfig


class QdrantClientManager:
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client: Optional[AsyncQdrantClient] = None

    def init_client(self):

        self.client = AsyncQdrantClient(
            url=f"http://{self.config.host}:{self.config.port}",
            trust_env=False,
        )

    async def close(self):
        await self.client.close()

qdrant_client_manager = QdrantClientManager(app_config.qdrant)

if __name__ == '__main__':
    async def test():

        qdrant_client_manager.init_client()
        client = qdrant_client_manager.client

        collection_name = "my_collection"

        if  await client.collection_exists(collection_name=collection_name):
            await client.delete_collection(collection_name=collection_name)
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size = app_config.qdrant.embedding_size,
                distance=models.Distance.COSINE
            )
        )

        await client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=i,
                    payload={
                        "color": "red" if i % 2 == 0 else "blue",
                    },
                    vector=[random.random() for i in range(1024)],
                )
                for i in range(10)
            ],
        )

        result = await client.query_points(
            collection_name=collection_name,
            query=[random.random() for i in range(1024)],
            limit=5,  # 取Top5
            score_threshold=0.6,  # 相似度得分的最小值
            query_filter=models.Filter(  # 根据payload进行过滤
                must=[models.FieldCondition(key="color", match=models.MatchValue(value="blue"))]
            ),
        )

        points = result.points
        print(points)
        for point in points:
            print(point.payload)

        await  qdrant_client_manager.close()
    asyncio.run(test())

