import uasyncio as asyncio


class AsyncTestRunner:
    def __init__(self):
        self.return_value = None

    async def _runner(self, coro):
        self.return_value = await coro

    def run(self, coro):
        asyncio.get_event_loop().run_until_complete(self._runner(coro))
        return self.return_value


class Mock:
    def __init__(self):
        self.calls = []
        self.return_value = None

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.return_value:
            return self.return_value

    @property
    def call_args_list(self):
        return self.calls


def AsyncMock(*args, **kwargs):
    m = Mock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro
