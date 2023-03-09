from functools import partial
import logging

from p4p.client.thread import Context

from EPICSPyClientPerformance.monitor_client import MonitorClient

#logging.getLogger("p4p").setLevel("INFO")
#logging.getLogger("p4p.client.thread").setLevel("DEBUG")

class P4PMonitor(MonitorClient):
    def __init__(self):
        super(P4PMonitor, self).__init__()
        self._subscriptions = []
        self._ctxt = Context("pva")

    def create_monitors(self):
        for pv_name in self._pv_names:
            cb = partial(self.callback, pv_name)
            self._subscriptions.append(self._ctxt.monitor(pv_name, cb))

    def callback(self, pv_name, value):
        super().callback(pv_name)
            
        if (self.is_active):
            self.add_sample(pv_name, value, value.timestamp, value.severity)

    def close(self):
        for sub in self._subscriptions:
            sub.close()
        self._ctxt.close()
