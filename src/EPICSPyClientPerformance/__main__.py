import argparse
import logging
import math
import time
from datetime import datetime

import psutil

from . import __version__

__all__ = ["main"]


# Setup the command line options for the client tests
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--debug",
        choices=[
            logging.getLevelName(logging.CRITICAL),
            logging.getLevelName(logging.ERROR),
            logging.getLevelName(logging.WARNING),
            logging.getLevelName(logging.INFO),
            logging.getLevelName(logging.DEBUG),
            logging.getLevelName(logging.NOTSET),
        ],
        default=logging.getLevelName(logging.INFO),
        help="Set the debug level ({})".format(logging.getLevelName(logging.INFO)),
    )
    parser.add_argument(
        "-r", "--records", default=1, help="Number of PVs to monitor (1)"
    )
    parser.add_argument(
        "-p", "--prefix", default="TEST:CALC", help="Record name prefix (TEST:CALC)"
    )
    parser.add_argument(
        "-s",
        "--samples",
        default=100,
        help="Number of samples per monitor to collect (100)",
    )
    parser.add_argument(
        "-u",
        "--update",
        default=0.1,
        help="Sample update period in seconds (0.1)"
    )
    parser.add_argument(
        "-c",
        "--client",
        choices=["pyepics", "caproto", "aioca", "p4p", "p4pasync", "p4pcothread", "pvapy", "cothread", "cachannel", "cachannel.ca"],
        default="pyepics",
        help="Client type to test",
    )
    args = parser.parse_args()
    return args


def main():
    args = options()
    logging.basicConfig(format="%(asctime)s %(message)s", level=args.debug)
    args.records = int(args.records)
    test_samples = int(args.samples)
    total_samples = test_samples * args.records
    update_freq = 1/float(args.update)

    # Simple argh check to choose which test to run
    mon = None
    if args.client == "pyepics":
        from EPICSPyClientPerformance.pyepics_monitor import PyEPICSMonitor

        mon = PyEPICSMonitor()
    elif args.client == "caproto":
        from EPICSPyClientPerformance.caproto_monitor import CAProtoMonitor

        mon = CAProtoMonitor()
    elif args.client == "aioca":
        from EPICSPyClientPerformance.aioca_monitor import AiocaMonitor

        mon = AiocaMonitor()
    elif args.client == "p4p":
        from EPICSPyClientPerformance.p4p_monitor import P4PMonitor

        mon = P4PMonitor()
    elif args.client == "p4pasync":
        from EPICSPyClientPerformance.p4p_async_monitor import P4PMonitorAsync

        mon = P4PMonitorAsync()
    elif args.client == "p4pcothread":
        from EPICSPyClientPerformance.p4p_cothread_monitor import P4PCothreadMonitor

        mon = P4PCothreadMonitor()
    elif args.client == "pvapy":
        from EPICSPyClientPerformance.pvapy_monitor import PvapyMonitor

        mon = PvapyMonitor()
    elif args.client == "cothread":
        from EPICSPyClientPerformance.cothread_monitor import CothreadMonitor

        mon = CothreadMonitor()
    elif args.client == "cachannel":
        from EPICSPyClientPerformance.cachannel_monitor import CaChannelMonitor

        mon = CaChannelMonitor()
    elif args.client == "cachannel.ca":
        from EPICSPyClientPerformance.cachannel_ca_monitor import CaChannelCaMonitor

        mon = CaChannelCaMonitor()

    process = psutil.Process()
    cpu_samples = []
    
    # Now run the camonitor process until the correct number of samples
    # have been collected
    mon.monitor_pv(args.prefix, args.records, test_samples)

    # Sleep long enough for the monitors to all be established
    #time.sleep(15)
         
    # Sample CPU here a couple of times and throw away so that we don't
    # include any module import or setting up in the CPU monitoring
    for i in range(2):
        cpu = process.cpu_percent(interval=1)
    
    # Activate the monitors to start saving data
    mon.activate()
    monitors_completed = False
    iteration = 0
        
    while monitors_completed is False:
        cpu = process.cpu_percent(interval=1)
        cpu_samples.append(cpu)
        iteration = iteration+1
        samples_collected = 0
        expected_samples = min(update_freq * args.records * iteration, total_samples)
        monitors_completed = True
        value_store = mon.results
        pv_names = mon.pv_names
        for pv_name in pv_names:
            if pv_name not in value_store:
                monitors_completed = False
            else:
                if len(value_store[pv_name]) < test_samples:
                    monitors_completed = False
                samples_collected += len(value_store[pv_name])

        if mon.connected_counter < args.records:
            logging.warn(
                "Warning: {} records not yet connected".format(
                    args.records-mon.connected_counter)
            )
        if (samples_collected < expected_samples):
            logging.warn(
                "Monitor backlog detected: {} samples behind expected number".format(
                    int(expected_samples-samples_collected))
            )
        logging.info(
            "Snapshot CPU [{}] Collected {} out of {} total samples".format(
                cpu, samples_collected, test_samples * len(pv_names)
            )
        )

    cpu_mean = sum(cpu_samples) / len(cpu_samples)
    cpu_std = math.sqrt(
        sum((x - cpu_mean) ** 2 for x in cpu_samples) / len(cpu_samples)
    )

    # Samples have been collected, now verify each individual
    # value to check there are no missing samples
    value_store = mon.results
    pv_names = mon.pv_names
    errors_counted = 0
    for pv_name in pv_names:
        if pv_name not in value_store:
            logging.error("Failed to receive a monitor for {}".format(pv_name))
            errors_counted = 0
        else:
            data = value_store[pv_name]
            expected_value = data[0]["value"]
            expected_time = 0.0
            expected_severity = 1
            for index in range(test_samples):
                if expected_value != data[index]["value"]:
                    logging.error(
                        "{}: Data error detected. Expected {} and got {}".format(
                            pv_name, expected_value, data[index]["value"]
                        )
                    )
                    errors_counted += 1
                    expected_value = data[index]["value"]
                expected_value += 1
                if expected_time >= data[index]["timestamp"]:
                    logging.error(
                        "{}: Timestamp error detected. Expected >={} and got {}".format(
                            pv_name, expected_time, data[index]["timestamp"]
                        )
                    )
                    errors_counted += 1
                expected_time = data[index]["timestamp"]
                if expected_severity != data[index]["severity"]:
                    logging.error(
                        "{}: Severity error detected. Expected {} and got {}".format(
                            pv_name, expected_severity, data[index]["severity"]
                        )
                    )
                    errors_counted += 1

    logging.info("Completed verification, errors: {}".format(errors_counted))
    logging.info("CPU: Mean {} [STD {}]".format(cpu_mean, cpu_std))
    
    # Log the time difference between the first PV to start receiving callbacks and the last
    min_time = min([value_store[pv_name][0]["timestamp"] for pv_name in pv_names])
    max_time = max([value_store[pv_name][0]["timestamp"] for pv_name in pv_names])
    time_difference = datetime.fromtimestamp(max_time) - datetime.fromtimestamp(min_time)
    logging.info("Maximum timestamp difference between first samples: {} seconds".format(
        time_difference.total_seconds()
        )
    )

    # Shut down the monitors and clean up
    mon.close()


# test with: python -m EPICSPyClientPerformance
if __name__ == "__main__":
    main()
