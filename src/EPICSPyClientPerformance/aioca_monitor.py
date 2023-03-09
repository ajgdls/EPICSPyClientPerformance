import asyncio
from threading import Thread

from aioca import FORMAT_TIME, camonitor

from EPICSPyClientPerformance.monitor_client import MonitorClient


class AiocaMonitor(MonitorClient):
    def __init__(self):
        super().__init__()
        self._thread = None
        self._finished = None

    def create_monitors(self):
        self._thread = Thread(target=asyncio.run, args=(self.run_loop(),))
        self._thread.start()

    async def run_loop(self):
        self._finished = asyncio.Event()
        subscriptions = camonitor(self._pv_names, self.callback, format=FORMAT_TIME)
        await self._finished.wait()
        for sub in subscriptions:
            sub.close()

    def callback(self, value, index):
        pv_name = self.pv_names[index]
        super().callback(pv_name)
        
        if (self.is_active):    
            self.add_sample(pv_name, value, value.timestamp, value.severity)

    def close(self):
        asyncio.get_event_loop().call_soon_threadsafe(self._finished.set())
        self._thread.join()
