from epics import camonitor

from EPICSPyClientPerformance.monitor_client import MonitorClient


client = None

# Create the monitor callback
def pyepics_callback(pvname, value, char_value, **kw):
    client.add_sample(pvname, value, kw['timestamp'], kw['severity'])


class PyEPICSMonitor(MonitorClient):
    def __init__(self):
        super(PyEPICSMonitor, self).__init__()
        self._subscriptions = []
        global client
        client = self

    def create_monitors(self):
        for pv_name in self._pv_names:
            sub = camonitor(pv_name, writer=None, callback=pyepics_callback)
            self._subscriptions.append(sub)

