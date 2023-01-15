
import asyncio

async def countdown(n):
    while n > 0:
        print(n)
        n -= 1
        await asyncio.sleep(1)
    print("timer end")

async def test():
    task = asyncio.create_task(countdown(5))
    print("timer start")
    await task

