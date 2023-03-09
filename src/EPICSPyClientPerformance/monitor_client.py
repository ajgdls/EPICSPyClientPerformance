import logging

class MonitorClient(object):
        
    def __init__(self):
        self._pv_names = []
        self._value_store = {}
        self._records = 1
        self._samples = 1
        self._active = False # Monitors should only store values when activated
        self._connected_list = {}
        
    def monitor_pv(self, prefix, records, samples):
        self._records = records
        self._samples = samples
        # Build the PV subscription list
        for pv_index in range(records):
            pv_name = "{}{:05d}".format(prefix, pv_index)
            self._pv_names.append(pv_name)
            self._value_store[pv_name] = []
            self._connected_list[pv_name] = False

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
    
    def callback(self, pv_name):
        # First time we are called back register that we are connected
        if not self._connected_list[pv_name]:
            self._connected_list[pv_name] = True
            logging.debug(
                "PV [{}] now connected".format(
                    pv_name
                )
            )
    
    def activate(self):
        self._active = True
        
    @property
    def is_active(self):
        return self._active
               
    @property
    def connected_counter(self):
        return sum(self._connected_list[pv] == True for pv in self.pv_names)

    @property
    def pv_names(self):
        return self._pv_names

    def create_monitors(self):
        raise RuntimeError("create_monitors has not been implemented")

    @property
    def results(self):
        return self._value_store
