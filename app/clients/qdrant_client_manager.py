from typing import Optional

from qdrant_client import AsyncQdrantClient


from app.conf.app_config import app_config
from app.conf.app_config import QdrantConfig


class QdrantClientManager:
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client: Optional[AsyncQdrantClient] = None

    def init_client(self):
        self.client = AsyncQdrantClient("localhost")

    async def close(self):
        await self.client.close()

qdrant_client_manager = QdrantClientManager(app_config.qdrant)

if __name__ == '__main__':

    qdrant_client_manager.init_client()
    client = qdrant_client_manager.client

    collection_name = "my_collection"

    if not await client.collection_exists(collection_name=collection_name):
        collection = await client.create_collection(collection_name=collection_name)