from functools import partial

import pvaccess

from EPICSPyClientPerformance.monitor_client import MonitorClient


class PvapyMonitor(MonitorClient):
    def __init__(self):
        super(PvapyMonitor, self).__init__()
        self._subscriptions = []

    def create_monitors(self):
        for pv_name in self._pv_names:
            cb = partial(self.callback, pv_name)
            c = pvaccess.Channel(pv_name)
            c.subscribe(pv_name, cb)
            c.startMonitor("field(value,alarm,timeStamp)")
            self._subscriptions.append(c)

    def callback(self, pv_name, value):
        super().callback(pv_name)
            
        if (self.is_active):
            self.add_sample(
                pv_name,
                value["value"],
                value["timeStamp"]["secondsPastEpoch"]
                + float(value["timeStamp"]["nanoseconds"]) / 1000000000,
                value["alarm"]["severity"],
            )

    def close(self):
        for sub, pv_name in zip(self._subscriptions, self._pv_names):
            sub.stopMonitor()
            sub.unsubscribe(pv_name)
