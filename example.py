#!/usr/bin/env python3
#coding=UTF-8
import processdog
import logging

if __name__ == '__main__':
    # Set up logger
    logger = logging.getLogger('processdog')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(threadName)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    """Create a ManagerThread object with 3 threads that
    polls 1 time per second
    """
    manager = processdog.ManagerThread(3, poll=1)

    """First three sleep commands will complete successfully,
    the second 3 will be killed after the timeout of 6 seconds.
    """
    for i in range(3):
        manager.jobs.put(['sleep', '4'])
    for i in range(3):
        manager.jobs.put(['sleep', '60'])
    manager.execute(timeout=6)

    """All the sleep commands will complete successfully due to the lack
    of a timeout argument.
    """
    for i in range(3):
        manager.jobs.put(['sleep', '4'])
    for i in range(3):
        manager.jobs.put(['sleep', '10'])
    manager.execute()
