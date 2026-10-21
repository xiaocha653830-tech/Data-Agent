from typing import TypedDict


class DataAgentState(TypedDict):
    query:str
    keyword:list[str]
    sql:str
    error:str