import logging
from functools import partial

from p4p.client.raw import Context

from EPICSPyClientPerformance.monitor_client import MonitorClient


class Callback:
    def __init__(self, callback, pv_name) -> None:
        self.callback = callback
        self.pv_name = pv_name

    def __call__(self):
        value = self.subscription.pop()
        while value is not None:
            self.callback(self.pv_name, value)
            value = self.subscription.pop()


class P4PRawMonitor(MonitorClient):
    def __init__(self):
        super(P4PRawMonitor, self).__init__()
        self._subscriptions = []
        self._ctxt = Context("pva", nt=False)

    def create_monitors(self):
        for pv_name in self._pv_names:
            cb = Callback(self.callback, pv_name)
            sub = self._ctxt.monitor(pv_name, cb)
            cb.subscription = sub
            self._subscriptions.append(sub)

    def callback(self, pv_name, value):
        super().callback(pv_name)

        if self.is_active:
            self.add_sample(
                pv_name,
                value["value"],
                value["timeStamp"]["secondsPastEpoch"]
                + value["timeStamp"]["nanoseconds"] / 1e9,
                value["alarm"]["severity"],
            )

    def close(self):
        for sub in self._subscriptions:
            sub.close()
        self._ctxt.close()
