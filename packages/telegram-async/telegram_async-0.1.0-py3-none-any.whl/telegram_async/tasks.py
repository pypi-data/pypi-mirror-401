import asyncio

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, coro, interval: int = None):
        """Dodaje zadanie async, opcjonalnie z interwałem (sekundy)"""
        async def looped():
            while True:
                await coro()
                if not interval:
                    break
                await asyncio.sleep(interval)
        t = asyncio.create_task(looped())
        self.tasks.append(t)
        return t

task_manager = TaskManager()
