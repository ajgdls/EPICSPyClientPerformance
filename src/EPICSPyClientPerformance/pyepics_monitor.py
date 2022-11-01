from epics import camonitor, camonitor_clear

from EPICSPyClientPerformance.monitor_client import MonitorClient


class PyEPICSMonitor(MonitorClient):
    def create_monitors(self):
        for pv_name in self._pv_names:
            camonitor(pv_name, writer=None, callback=self.callback)

    def callback(self, pvname, value, char_value, **kw):
        self.add_sample(pvname, value, kw["timestamp"], kw["severity"])

    def close(self):
        for pv_name in self._pv_names:
            camonitor_clear(pv_name)
