import asyncio
from typing import Optional

from langchain_huggingface import  HuggingFaceEndpointEmbeddings

from app.conf.app_config import app_config
from app.conf.app_config import EmbeddingConfig


class EmbeddingClientManager:
    def __init__(self,config:EmbeddingConfig):
        self.config = config
        self.client:Optional[HuggingFaceEndpointEmbeddings] = None

    def init_client(self):
        self.client = HuggingFaceEndpointEmbeddings(
            model=f"http://{self.config.host}:{self.config.port}"
        )

embedding_client_manager = EmbeddingClientManager(app_config.embedding)


if __name__ == '__main__':
    async def test():
        embedding_client_manager.init_client()

        vector: list[float] = await embedding_client_manager.client.aembed_query("hello")
        print(vector)
        print(len(vector))

        vectors: list[list[float]] = await embedding_client_manager.client.aembed_documents(["hello","world"])
        print(vectors)
        print(len(vectors), len(vectors[0]))

    asyncio.run(test())