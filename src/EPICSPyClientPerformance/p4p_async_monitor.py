from functools import partial
import logging
import asyncio
from threading import Thread

from p4p.client.asyncio import Context
from p4p import nt

from EPICSPyClientPerformance.monitor_client import MonitorClient


# Async IO version
class P4PMonitorAsync(MonitorClient):
      
    def __init__(self):
        super(P4PMonitorAsync, self).__init__()
        self._thread = None
        self._finished = None
        self._subscriptions = []
        self._counter = 0
        self._ctxt = Context("pva", nt=False) # NT set to false to disable wrapping

    def create_monitors(self):
        self._thread = Thread(target=asyncio.run, args=(self.run_loop(),))
        self._thread.start()
        
        
    async def run_loop(self):
        self._finished = asyncio.Event()
        for pv_name in self._pv_names:
            cb = partial(self.callback, pv_name)
            self._subscriptions.append(
                self._ctxt.monitor(
                    pv_name,
                    cb,
                    #request="record[queueSize=10]field(value,alarm,timeStamp)",
                )
            )
        
        await self._finished.wait()
        for sub in self._subscriptions:
            sub.close()


    async def callback(self, pv_name, value):
        super().callback(pv_name)
                
        if (self.is_active):
            self.add_sample(
                pv_name,
                value["value"],
                value["timeStamp"]["secondsPastEpoch"]
                + value["timeStamp"]["nanoseconds"] / 1e9,
                value["alarm"]["severity"],
            )

        # Alternative code for use with automatic wrapping:       
        # self.add_sample(
        #    pv_name,
        #    value,
        #    value.timestamp,
        #    value.severity,
        # )

    def close(self):
        asyncio.get_event_loop().call_soon_threadsafe(self._finished.set())        
        self._thread.join()
