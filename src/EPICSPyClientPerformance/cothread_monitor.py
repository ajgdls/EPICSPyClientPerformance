
import logging
from threading import Thread
import time

from EPICSPyClientPerformance.monitor_client import MonitorClient


cothread_client = None


# Create the monitor callback
def cothread_callback(value, index):
    pv_name = cothread_client._pv_names[index]
    logging.debug("PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(
        pv_name,
        value,
        value.timestamp,
        value.severity
        ))
    cothread_client.add_sample(
        pv_name,
        value,
        value.timestamp,
        value.severity
        )


class CothreadMonitor(MonitorClient):
    def __init__(self):
        super(CothreadMonitor, self).__init__()
        self._subscriptions = []
        self._task = None
        self._running = True
        global cothread_client
        cothread_client = self


    def create_monitors(self):
        self._task = Thread(target=self.run_loop)
        self._task.start()

    def run_loop(self):
        import cothread
        from cothread import Event
        from cothread.catools import camonitor, caget, FORMAT_TIME

#    def create_monitors(self):
        self._event = Event()
        self._subscriptions = camonitor(self._pv_names, cothread_callback, format=FORMAT_TIME)
#        for pv_name in self._pv_names:
            #logging.info("{}".format(caget(pv_name)))
#            cb = partial(pvapy_callback, pv_name)
#            c = pvaccess.Channel(pv_name)
#            c.subscribe(pv_name, cb)
#            c.startMonitor('field(value,alarm,timeStamp)')
#            self._subscriptions.append(c)
        while self._running:
            cothread.Sleep(1.0)
#            self._event.Wait()
        for sub in self._subscriptions:
            sub.close()
        self._subscriptions = None
        self._value_store = None

    def close(self):
        self._running = False
