import logging
from aioca import FORMAT_TIME, caget, camonitor, caput, run
import asyncio
from threading import Thread

from EPICSPyClientPerformance.monitor_client import MonitorClient


aioca_client = None


# Create the monitor callback
def aioca_callback(value, index):
    pv_name = aioca_client.pv_names[index]
    logging.debug("PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(pv_name, value, value.timestamp, value.severity))
    aioca_client.add_sample(pv_name, value, value.timestamp, value.severity)


class AiocaMonitor(MonitorClient):
    def __init__(self):
        super(AiocaMonitor, self).__init__()
        self._subscriptions = []
        self._running = True
        self._task = None
        global aioca_client
        aioca_client = self

    def create_monitors(self):
        self._task = Thread(target=self.run_loop)
        self._task.start()

    def run_loop(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        run(self.aioca_create_monitors(), forever=False)

    async def aioca_create_monitors(self):
        self._subscriptions = camonitor(self._pv_names, aioca_callback, format=FORMAT_TIME)
        while self._running:
            await asyncio.sleep(1)

    def close(self):
        for sub in self._subscriptions:
            sub.close()
        self._running = False
