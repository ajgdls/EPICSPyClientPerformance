from functools import partial
from threading import Thread
import logging
import time

from EPICSPyClientPerformance.monitor_client import MonitorClient

class P4PCothreadMonitor(MonitorClient):
    def __init__(self):
        super(P4PCothreadMonitor, self).__init__()
        self._subscriptions = []
        self._thread = None
        self._finished = None
           
    def create_monitors(self):
        self._thread = Thread(target=self.run_loop)
        self._thread.start()

    def run_loop(self):
        # Local import of cothread so it doesn't run in the main thread
        import cothread
        from p4p.client.cothread import Context
        self._ctxt = Context("pva")
        self._finished = cothread.Event(False)
               
        for pv_name in self._pv_names:
            cb = partial(self.callback, pv_name)
            # Note: notify_disconnect must be set to False for value updates to be received
            self._subscriptions.append(self._ctxt.monitor(pv_name, cb, notify_disconnect=False))
         
        self._finished.Wait()
        for sub in self._subscriptions:
            sub.close()
               
                  

    def callback(self, pv_name, value):
        super().callback(pv_name)
            
        if (self.is_active):
            self.add_sample(pv_name, value, value.timestamp, value.severity)

    def close(self):
        self._ctxt.close()
        import cothread

        cothread.Callback(self._finished.Signal)
        self._thread.join()
