import argparse
import logging

from softioc import asyncio_dispatcher, builder, softioc
from softioc.builder import records

from threading import Thread

import time

from . import __version__


# Setup the command line options for the example python IOC
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
        help="Set the debug level ({})".format(logging.getLevelName(logging.INFO))
    )
    parser.add_argument(
        "-r", "--records", default=1000, help="Number of records to create (1000)"
    )
    parser.add_argument(
        "-p", "--prefix", default="TEST", help="Record name prefix (TEST:)"
    )
    parser.add_argument(
        "-s", "--scan", default=1, help="Update rate in seconds (1)"
    )
    args = parser.parse_args()
    return args


class FastUpdateIOC:
    def __init__(self, numRecords, updateRate, prefix):
        self._thread = None
        self._records = []
        self._updateRate = updateRate
        
        # Set the record prefix
        builder.SetDeviceName(prefix)
        
        for r in range(numRecords):
            record = builder.aOut("CALC{:05d}".format(r), initial_value=0, always_update=True)
            record.HIGH = 1.0
            record.HSV = "MINOR"
            self._records.append(record)
    
        # Create the thread to update the values
        self._thread = Thread(target=self.run_loop)     
        


    def run_loop(self):
        counter = 1
        while(True):
            for record in self._records:
                record.set(counter, True)
            time.sleep(self._updateRate)
            counter = counter+1
            
    def start_updates(self):
        self._thread.start()
        

def start_updating():
    ioc.start_updates()
    
    

def main():
    args = options()
    logging.basicConfig(format="%(asctime)s %(message)s", level=args.debug)
    
    # Instantiate the IOC
    ioc = FastUpdateIOC(int(args.records), float(args.scan), args.prefix)
    globals()["ioc"] = ioc

    # Create an asyncio dispatcher, the event loop is now running
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()

    # Boilerplate get the IOC started
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    # Finally leave the IOC running with an interactive shell.
    softioc.interactive_ioc(globals())
        


if __name__ == "__main__":
    main()
