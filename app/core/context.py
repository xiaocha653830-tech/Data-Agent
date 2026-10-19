import asyncio
from _contextvars import ContextVar, Token


# 创建一个用于存储请求id的context_var对象
_req_context_var = ContextVar("request_id", default="")

#保存请求id
def set_request_id(request_id: str)->Token:
    return _req_context_var.set(request_id)

#获取请求id
def get_request_id():
    return _req_context_var.get()

#重置请求id
def reset_request_id(token:Token):
    _req_context_var.reset(token)

if __name__ == '__main__':
    async def req1():
        pass

    async def req2():
        pass

    async def test():
        await asyncio.gather(req1(),req2())