EPICSPyClientPerformance
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

.. note::

    This project contains template code only. For documentation on how to
    adopt this skeleton project see
    https://ajgdls.github.io/EPICSPyClientPerformance-cli

This is where you should write a short paragraph that describes what your module does,
how it does it, and why people should use it.

============== ==============================================================
PyPI           ``pip install EPICSPyClientPerformance``
Source code    https://github.com/ajgdls/EPICSPyClientPerformance
Documentation  https://ajgdls.github.io/EPICSPyClientPerformance
Releases       https://github.com/ajgdls/EPICSPyClientPerformance/releases
============== ==============================================================

This is where you should put some images or code snippets that illustrate
some relevant examples. If it is a library then you might put some
introductory code here:

.. code-block:: python

    from EPICSPyClientPerformance import __version__

    print(f"Hello EPICSPyClientPerformance {__version__}")

Or if it is a commandline tool then you might put some example commands here::

    $ python -m EPICSPyClientPerformance --version

.. |code_ci| image:: https://github.com/ajgdls/EPICSPyClientPerformance/actions/workflows/code.yml/badge.svg?branch=main
    :target: https://github.com/ajgdls/EPICSPyClientPerformance/actions/workflows/code.yml
    :alt: Code CI

.. |docs_ci| image:: https://github.com/ajgdls/EPICSPyClientPerformance/actions/workflows/docs.yml/badge.svg?branch=main
    :target: https://github.com/ajgdls/EPICSPyClientPerformance/actions/workflows/docs.yml
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/ajgdls/EPICSPyClientPerformance/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/ajgdls/EPICSPyClientPerformance
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/EPICSPyClientPerformance.svg
    :target: https://pypi.org/project/EPICSPyClientPerformance
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://ajgdls.github.io/EPICSPyClientPerformance for more detailed documentation.

Example Test Result
===================

Test monitoring 100 records at 10 Hz, collecting 1000 Samples.

IOC running on Intel(R) Xeon(R) CPU E5-2430L 0 @ 2.00GHz (12 core)
Client running on Intel(R) Xeon(R) CPU E5-1630 v3 @ 3.70GHz (4 core)
Python 3.8

========  ========  ========  =======  =======  ========
Client Tests
--------------------------------------------------------
Client    Version   Rate(Hz)  Records  Samples  CPU(%)
========  ========  ========  =======  =======  ========
pyepics   3.5.1     10        100      1000     4.7
caproto   0.8.1     10        100      1000     9.4
aioca     1.4       10        100      1000     10.2
p4p       4.1.0     10        100      1000     11.7
pvapy     5.1.0     10        100      1000     3.2
cothread  2.18.1    10        100      1000     3.0
========  ========  ========  =======  =======  ========
