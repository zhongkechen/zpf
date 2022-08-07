
from .pool import SimpleEventPool


async def async_main():
    pass


def main():
    return SimpleEventPool.run(async_main())
