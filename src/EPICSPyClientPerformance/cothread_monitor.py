from threading import Thread

from EPICSPyClientPerformance.monitor_client import MonitorClient


class CothreadMonitor(MonitorClient):
    def __init__(self):
        super().__init__()
        self._thread = None
        self._finished = None

    def create_monitors(self):
        self._thread = Thread(target=self.run_loop)
        self._thread.start()

    def run_loop(self):
        # Local import of cothread so it doesn't run in the main thread
        import cothread
        from cothread.catools import FORMAT_TIME, camonitor

        self._finished = cothread.Event()
        subscriptions = camonitor(self._pv_names, self.callback, format=FORMAT_TIME)
        self._finished.Wait()
        for sub in subscriptions:
            sub.close()

    def callback(self, value, index):
        pv_name = self._pv_names[index]
        super().callback(pv_name)
        
        if self.is_active:
            self.add_sample(pv_name, value, value.timestamp, value.severity)

    def close(self):
        import cothread

        cothread.Callback(self._finished.Signal)
        self._thread.join()
