import argparse
import asyncio
import logging
from datetime import datetime, timedelta

from softioc import asyncio_dispatcher, builder, softioc
from softioc.builder import records

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
    args = parser.parse_args()
    return args


def main():
    args = options()
    logging.basicConfig(format="%(asctime)s %(message)s", level=args.debug)
    args.records = int(args.records)

    # Create an asyncio dispatcher, the event loop is now running
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()

    # Set the record prefix
    builder.SetDeviceName(args.prefix)

    # Create some records
    record_store = []
    for index in range(args.records):
        calc = records.calc("CALC{:05d}".format(index), CALC="A+1", SCAN=".1 second")
        calc.INPA = builder.NP(calc)
        record_store.append(calc)

    # Boilerplate get the IOC started
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    # Finally leave the IOC running with an interactive shell.
    softioc.interactive_ioc(globals())


if __name__ == "__main__":
    main()
