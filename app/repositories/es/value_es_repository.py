from elasticsearch import AsyncElasticsearch

from app.models.es.value_info_es import ValueInfoES

"""
用于操作es数据库中字段值的持久层模块
"""

class ValueESRepository:
    index_name = "data-agent-value_index2"
    mappings = {
        "dynamic": False,
        "properties": {
            "id": {"type": "keyword","index":False},
            "value": {"type": "text", "analyzer": "ik_max_word"},
            "type": {"type": "keyword","index":False},
            "column_id": {"type": "keyword","index":False},
            "column_name": {"type": "keyword","index":False},
            "table_id": {"type": "keyword","index":False},
            "table_name": {"type": "keyword","index":False},
        }
    }

    def __init__(self,client: AsyncElasticsearch):
        self.client = client


    async def create_index(self):
        client = self.client
        index_name = self.index_name
        mappings = self.mappings

        # 创建索引   如果存在先删除
        if await client.indices.exists(index=index_name):
            await client.indices.delete(index=index_name)
        await client.indices.create(
            index=index_name,
            mappings=mappings
        )

    #批量保存多个字段值信息
    async def insert_value_info(self, value_infos: list[ValueInfoES]):
        client = self.client
        index_name = self.index_name

        await self.create_index()

        batch_size = 50
        for i in range(0, len(value_infos), batch_size):
            batch_value_infos = value_infos[i:i+batch_size]

            operations = []
            for value_info in batch_value_infos:
                operations.append(
                    {
                        "index": {
                            "_index": index_name
                        }
                    }
                )
                operations.append(value_info)


            # 批量插入多个文档
            await client.bulk(operations=operations)