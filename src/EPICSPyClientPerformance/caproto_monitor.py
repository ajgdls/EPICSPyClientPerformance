import logging

from caproto.threading.client import Context

from EPICSPyClientPerformance.monitor_client import MonitorClient

# Turn off caproto broadcast logging messages
logging.getLogger("caproto").setLevel("CRITICAL")


class CAProtoMonitor(MonitorClient):
    def __init__(self):
        super(CAProtoMonitor, self).__init__()
        self._subscriptions = []
        self._ctx = Context()

    def create_monitors(self):
        pvs = self._ctx.get_pvs(*self._pv_names)
        for pv in pvs:
            sub = pv.subscribe(data_type="time")
            sub.add_callback(self.callback)
            self._subscriptions.append(sub)

    def callback(self, sub, value):
        super().callback(sub.pv.name)
            
        if (self.is_active):
            self.add_sample(
                sub.pv.name,
                value.data[0],
                value.metadata.timestamp,
                value.metadata.severity,
            )

    def close(self):
        for sub in self._subscriptions:
            sub.clear()
        self._ctx.disconnect()
