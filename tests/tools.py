import uasyncio as asyncio


class AsyncTestRunner:
    def __init__(self):
        self.return_value = None

    async def _runner(self, coro):
        self.return_value = await coro

    def run(self, coro):
        asyncio.get_event_loop().run_until_complete(self._runner(coro))
        return self.return_value
