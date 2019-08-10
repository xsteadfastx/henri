async def foo():
    return "bar"


async def bar():
    return await foo()
