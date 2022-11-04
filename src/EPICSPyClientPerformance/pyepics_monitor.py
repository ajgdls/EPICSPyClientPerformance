from epics import camonitor_clear, get_pv

from EPICSPyClientPerformance.monitor_client import MonitorClient


class PyEPICSMonitor(MonitorClient):
    def create_monitors(self):
        self.pvs = [get_pv(name, callback=self.callback) for name in self._pv_names]

    def callback(self, pvname, value, char_value, **kw):
        self.add_sample(pvname, value, kw["timestamp"], kw["severity"])

    def close(self):
        for pv_name in self._pv_names:
            camonitor_clear(pv_name)
