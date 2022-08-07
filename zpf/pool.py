import asyncio
from threading import Thread


class SimpleEventPool:
    loop = None
    thread = None
    busy = 0

    @classmethod
    def _init(cls):
        if not cls.loop:
            cls.loop = asyncio.get_event_loop()
            cls.thread = Thread(target=cls.loop.run_forever)
            cls.thread.daemon = True
            cls.thread.start()

    @classmethod
    def run(cls, coro, background=False):
        if not cls.loop:
            cls._init()

        future = asyncio.run_coroutine_threadsafe(coro, cls.loop)
        if not background:
            return future.result()
        else:
            return future

    @classmethod
    def shutdown(cls):
        if cls.loop:
            cls.loop.stop()

    @classmethod
    def join(cls, timeout=None):
        if cls.thread:
            cls.thread.join(timeout=timeout)
