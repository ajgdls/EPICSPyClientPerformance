
import logging
from functools import partial
import pvaccess
import time

from EPICSPyClientPerformance.monitor_client import MonitorClient


pvapy_client = None


# Create the monitor callback
def pvapy_callback(pv_name, value):
    logging.debug("PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(
        pv_name,
        value['value'],
        value['timeStamp']['secondsPastEpoch'] + float(value['timeStamp']['nanoseconds'])/1000000000,
        value['alarm']['severity']
        ))
    pvapy_client.add_sample(
        pv_name,
        value['value'],
        value['timeStamp']['secondsPastEpoch'] + float(value['timeStamp']['nanoseconds'])/1000000000,
        value['alarm']['severity']
        )


class PvapyMonitor(MonitorClient):
    def __init__(self):
        super(PvapyMonitor, self).__init__()
        self._subscriptions = []
        global pvapy_client
        pvapy_client = self

    def create_monitors(self):
        for pv_name in self._pv_names:
            cb = partial(pvapy_callback, pv_name)
            c = pvaccess.Channel(pv_name)
            c.subscribe(pv_name, cb)
            c.startMonitor('field(value,alarm,timeStamp)')
            self._subscriptions.append(c)

    def close(self):
        for sub, pv_name in zip(self._subscriptions, self._pv_names):
            sub.stopMonitor()
            sub.unsubscribe(pv_name)
