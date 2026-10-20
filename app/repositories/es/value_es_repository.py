from elasticsearch import AsyncElasticsearch


"""
用于操作es数据库中字段值的持久层模块
"""

class ValueESRepository:
    def __init__(self,client: AsyncElasticsearch):
        self.client = client