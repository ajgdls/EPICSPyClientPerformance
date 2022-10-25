
import logging
from functools import partial
from p4p.client.thread import Context

from EPICSPyClientPerformance.monitor_client import MonitorClient


p4p_client = None


# Create the monitor callback
def p4p_callback(pv_name, value):
    logging.debug("PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(pv_name, value, value.timestamp, value.severity))
    p4p_client.add_sample(pv_name, value, value.timestamp, value.severity)


class P4PMonitor(MonitorClient):
    def __init__(self):
        super(P4PMonitor, self).__init__()
        self._subscriptions = []
        self._ctxt = Context('pva')
        global p4p_client
        p4p_client = self

    def create_monitors(self):
        for pv_name in self._pv_names:
            cb = partial(p4p_callback, pv_name)
            self._subscriptions.append(self._ctxt.monitor(pv_name, cb))

    def close(self):
        for sub in self._subscriptions:
            sub.close()
