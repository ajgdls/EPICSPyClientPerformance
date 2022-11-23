from CaChannel import ca, CaChannel

from EPICSPyClientPerformance.monitor_client import MonitorClient

class CaChannelMonitor(MonitorClient):
    def create_monitors(self):
        self._channels = []
        for pv_name in self._pv_names:
            channel = CaChannel()
            channel.search_and_connect(pv_name, self._connect_callback, channel)

            self._channels.append(channel)
        ca.flush_io()

    def _connect_callback(self, epics_args, user_args):
        connect_state = epics_args[1] 
        channel = user_args[0]
        if connect_state == ca.CA_OP_CONN_UP:
            channel.add_masked_array_event(
                    ca.dbf_type_to_DBR_TIME(channel.field_type()),
                    None,
                    None, 
                    self.callback,
                    channel)
            ca.flush_io()

    def callback(self, epics_args, user_args):
        channel = user_args[0]
        self.add_sample(
                channel.name(),
                epics_args['pv_value'],
                epics_args['pv_seconds'] + ca.POSIX_TIME_AT_EPICS_EPOCH + epics_args['pv_nseconds']*1e-9,
                epics_args['pv_severity'])

    def close(self):
        for channel in self._channels:
            channel.clear_channel()
