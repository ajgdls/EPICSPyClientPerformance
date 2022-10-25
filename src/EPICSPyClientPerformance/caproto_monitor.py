import logging
from caproto.threading.client import Context

from EPICSPyClientPerformance.monitor_client import MonitorClient

# Turn off caproto broadcast logging messages
logging.getLogger('caproto').setLevel('CRITICAL')
client = None


# Create the monitor callback
def caproto_callback(sub, value):
    logging.debug("PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(sub.pv.name, value.data[0], value.metadata.timestamp, value.metadata.severity))
    client.add_sample(sub.pv.name, value.data[0], value.metadata.timestamp, value.metadata.severity)

class CAProtoMonitor(MonitorClient):
    def __init__(self):
        super(CAProtoMonitor, self).__init__()
        self._subscriptions = []
        self._ctx = Context()
        global client
        client = self

    def create_monitors(self):
        for pv_name in self._pv_names:
            pvs = self._ctx.get_pvs(pv_name)
            pv = pvs[0]
            pv.read(data_type='time')
            sub = pv.subscribe(data_type='time')
            sub.add_callback(caproto_callback)
            self._subscriptions.append(sub)

