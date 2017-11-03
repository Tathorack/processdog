================================
processdog - Subprocess Watchdog
================================

|python35| |license| |format|

.. |python35| image:: https://img.shields.io/badge/Python-3.5-brightgreen.svg
    :target: https://www.python.org/
.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://github.com/Tathorack/imagecolor/blob/master/LICENSE.md
.. |format| image:: https://img.shields.io/pypi/format/imagecolor.svg
    :target: https://pypi.python.org/pypi/imagecolor

------------------------------------------------------------------------------------
This module uses python threads to manage subprocesses and kill them if they timeout
------------------------------------------------------------------------------------

Available classes
=================
Manager(num_threads, jobs=None, poll=1)
=======================================
Creates a manager thread object that can then be be given a queue of subprocess commands to execute

Initialization paramaters

* ``num_threads`` - maximum number of threads to
* ``jobs`` - queue.Queue object containg the subprocess commands to execute. Defaults to empty if not set.
* ``poll`` - how often to poll the worker threads to see if they have completed or timedout. Defaults to 1 second.

Class methods

* ``addjob(job)`` - adds a job to the queue

Usage example
=============

.. code:: python

    import processdog
    manager = processdog.ManagerThread(2, poll=1)
        manager.addjob(['sleep', '4'])
        manager.addjob(['sleep', '60'])
    manager.execute(timeout=6)

This will spawn two worker threads to complete the commands. The first sleep will complete normally and the second will be killed after 6 seconds

A more detailed example that includes logging is contained in example.py
