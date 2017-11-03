#!/usr/bin/env python3
# coding=UTF-8
import logging
import queue
import subprocess
import threading
import time

logger = logging.getLogger(__name__)


class WorkerThread(threading.Thread):
    """Subclass of Thread that allows a thread to be spawned that runs a
    subprocess. This allows the subprocess to be killed off by the main
    ManagerThread if the thread takes too long to complete.
    """
    def __init__(self, thread_id, job_queue):
        """Get a thread ID and a subprocess command from a job queue.
        Target function runs when
        """
        self.process = None
        self.thread_id = thread_id
        self.job_queue = job_queue
        self.cmd = self.job_queue.get()
        self.start_time = time.time()

        def target():
            logger.info('Subprocess started')
            self.process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            self.process.communicate()
            self.finished = True
            self.job_queue.task_done()
            logger.info('Subprocess finished')
        super().__init__(name='Thread-{}'.format(self.thread_id),
                         target=target)
        self.finished = False
        logger.debug('Thread %d Initialized', self.thread_id)

    def kill_process(self):
        if self.is_alive():
            logger.warning('Terminating subprocess on Thread-%d',
                           self.thread_id)
            self.process.terminate()
            self.finished = True


class ManagerThread(object):
    def __init__(self, num_threads, jobs=None, poll=1):
        if num_threads < 1:
            raise ValueError('Number of threads must be greater than 1')
        if jobs is None:
            self.jobs = queue.Queue()
        else:
            self.jobs = jobs
        self.lock = threading.Lock()
        self.free = []
        self.running = []
        for t in range(num_threads):
            self.free.append(t)
        self.poll = poll

    def execute(self, timeout=None):
        logger.info('Manager execution starting')
        while True:
            if timeout is not None:
                with self.lock:
                    """Kill threads that have been running for
                    longer than the timeout period. Add their
                    ID's to the pool of free threads.
                    """
                    logger.debug('checking for timedout threads')
                    for thread in self.running:
                        if time.time() - thread.start_time > timeout:
                            thread.kill_process()
                            if thread.finished:
                                self.running.remove(thread)
                                self.free.append(thread.thread_id)
                                thread.join()

            with self.lock:
                """Clean up finished threads. Add
                ID's to the pool of free threads.
                """
                logger.debug('Checking for finished threads')
                for thread in self.running:
                    if thread.finished:
                        self.running.remove(thread)
                        self.free.append(thread.thread_id)
                        thread.join()

            while not self.jobs.empty() and len(self.free) > 0:
                """If there are jobs remaining and free threads then
                spawn new threads for each pair of jobs and threads.
                """
                with self.lock:
                    if len(self.free) > 0:
                        thread_id = self.free.pop()
                        thread = WorkerThread(
                            thread_id, self.jobs)
                        self.running.append(thread)
                        thread.start()

            if self.jobs.empty() and len(self.running) == 0:
                logger.info('Manager execution finished')
                break
            logger.debug('Sleeping for %d', self.poll)
            time.sleep(self.poll)

    def addjob(self, job):
        self.jobs.put(job)
