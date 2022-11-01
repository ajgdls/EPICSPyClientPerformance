import logging


class MonitorClient(object):
    def __init__(self):
        self._pv_names = []
        self._value_store = {}
        self._records = 1
        self._samples = 1

    def monitor_pv(self, prefix, records, samples):
        self._records = records
        self._samples = samples
        # Build the PV subscription list
        for pv_index in range(records):
            pv_name = "{}{:05d}".format(prefix, pv_index)
            self._pv_names.append(pv_name)
            self._value_store[pv_name] = []

        self.create_monitors()

    def add_sample(self, pvname, value, timestamp, severity):
        logging.debug(
            "PV [{}] Value: {}  Timestamp: {}  Severity: {}".format(
                pvname, value, timestamp, severity
            )
        )
        # Assign value
        item = {"value": value, "timestamp": timestamp, "severity": severity}
        if len(self._value_store[pvname]) < self._samples:
            self._value_store[pvname].append(item)

    def close(self):
        pass

    @property
    def pv_names(self):
        return self._pv_names

    def create_monitors(self):
        raise RuntimeError("create_monitors has not been implemented")

    @property
    def results(self):
        return self._value_store
