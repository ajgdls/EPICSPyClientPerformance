EPICSPyClientPerformance
===========================

A set of performance tests for multiple Python EPICS clients.

The CPU usage of the process is recorded whilst monitoring
a set of EPICS records.


Installation
============

These tests compile and run with Python 3.8+

To install

.. code-block:: bash

    git clone https://github.com/ajgdls/EPICSPyClientPerformance
    cd EPICSPyClientPerformance
    python -m venv venv   #(must be python 3.8)
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .[dev]


Execution
=========

The test creates a set of monitors for the chosen client type to monitor a
set of calcout records that are incrementing their value by 1 at a rate of
10 Hz.  An example IOC that contains the required records can be started
with the following command:


.. code-block:: bash

    example_ioc -h
    usage: example_ioc [-h] [--version] [--debug {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}] [-r RECORDS] [-p PREFIX]

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    --debug {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
                            Set the debug level (INFO)
    -r RECORDS, --records RECORDS
                            Number of records to create (1000)
    -p PREFIX, --prefix PREFIX
                            Record name prefix (TEST:)


The IOC will start with the number of records specified and each record
will count up at a rate of 10 Hz.  The severity of each record will
immediately fall into MINOR alarm.


Once the IOC is operational run the client with the following command:


.. code-block:: bash

    client_test -h
    usage: client_test [-h] [--version] [--debug {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}] [-r RECORDS] [-p PREFIX] [-s SAMPLES]
                    [-c {pyepics,caproto,aioca,p4p,pvapy,cothread}]

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    --debug {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
                            Set the debug level (INFO)
    -r RECORDS, --records RECORDS
                            Number of PVs to monitor (1)
    -p PREFIX, --prefix PREFIX
                            Record name prefix (TEST:CALC)
    -s SAMPLES, --samples SAMPLES
                            Number of samples per monitor to collect (100)
    -c {pyepics,caproto,aioca,p4p,pvapy,cothread}, --client {pyepics,caproto,aioca,p4p,pvapy,cothread}
                            Client type to test


The test script will create monitors (1 monitor on each record up to the
number of specified records).  For each monitor update the value, severity
and timestamp of the update is recorded.  While the test is active the CPU
usage of the process is monitored and snapshots recorded.

Once all samples from all monitors have been collected then the test stops
monitoring CPU and calculates the average.  Finally checks are made on each
of the samples collected to ensure no expected values are missing, no
timestamps are unexpected (in the past, not updated) and the severity of
MINOR has been recorded with each sample.


Example Test Result
===================

Test monitoring 1000 records at 10 Hz, collecting 1000 Samples.

IOC running on Intel(R) Xeon(R) CPU E5-2430L 0 @ 2.00GHz (12 core)

.. code-block:: bash

    example_ioc -r 1000


Client running on Intel(R) Xeon(R) CPU E5-1630 v3 @ 3.70GHz (4 core)

.. code-block:: bash

    client_test -r 1000 -s 1000 -c cothread


Python 3.8

========  ========  ========  =======  =======  ========
Client Tests
--------------------------------------------------------
Client    Version   Rate(Hz)  Records  Samples  CPU(%)
========  ========  ========  =======  =======  ========
pyepics   3.5.1     10        1000     1000     45.9
caproto   0.8.1     10        1000     1000     70.0
aioca     1.4       10        1000     1000     62.2
p4p       4.1.0     10        1000     1000     73.8
pvapy     5.1.0     10        1000     1000     20.9
cothread  2.18.1    10        1000     1000     22.0
========  ========  ========  =======  =======  ========
