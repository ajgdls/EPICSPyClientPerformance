from CaChannel import ca

from EPICSPyClientPerformance.monitor_client import MonitorClient

class CaChannelCaMonitor(MonitorClient):
    def __init__(self):
        super().__init__()
        ca.create_context(preemptive_callback=True)

    def create_monitors(self):
        self._channels = []
        for pv_name in self._pv_names:
            status, channel = ca.create_channel(
                    pv_name,
                    callback=self._connect_callback)
            self._channels.append(channel)
        ca.flush_io()

    def _connect_callback(self, args):
        channel = args['chid']
        connect_state = args['op']
        if connect_state == ca.CA_OP_CONN_UP:
            ca.create_subscription(
                    channel,
                    self.callback,
                    chtype=ca.dbf_type_to_DBR_TIME(ca.field_type(channel)))
            ca.flush_io()

    def callback(self, args):
        self.add_sample(
                ca.name(args['chid']),
                args['value']['value'],
                args['value']['stamp']['timestamp'],
                args['value']['severity'])

    def close(self):
        for channel in self._channels:
            ca.clear_channel(channel)
        ca.flush_io()
        ca.destroy_context()
