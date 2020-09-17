import argparse
import logging
import queue
import threading
import time


class CommonThreadLogger:

    def __init__(self):
        pass

    def setup_basic(cls, format='%(threadName)s: %(message)s', level=logging.DEBUG):
        logging.basicConfig(level=level, format=format)

    def debug(self, msg):
        return logging.debug(msg)

    def info(self, msg):
        return logging.info(msg)


class CommonThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.args = list(args)
        self.kwargs = kwargs
        self.inq = queue.Queue()
        self.outq = queue.Queue()
        self.parser = argparse.ArgumentParser()
        self.params = {}
        self.elapsed = 0.0
        self.result = None

    def __repr__(self):
        return '{}(name={}, result={}, elapsed={}, args={}, kwargs={}, params={})'.format(
            self.__class__.__name__,
            self.name, self.result, self.elapsed, self.args, self.kwargs, self.params)

    def entry(self, *args, **kwargs):
        pass

    def run(self):
        t0 = time.time()
        self.result = self.entry(*self.args, **self.kwargs)
        t1 = time.time()
        self.elapsed = t1 - t0

    def join(self, timeout=None) -> bool:
        super().join(timeout=timeout)
        return not super().is_alive()

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self):
        str_array = []
        for p in self.args:
            str_array.append(str(p))
        ns = self.parser.parse_args(str_array)
        self.params = vars(ns)
        return self.params

    def output(self, item, block=True, timeout=None):
        assert threading.current_thread() == self
        return self.outq.put(item, block=block, timeout=timeout)

    def input(self, block=True, timeout=None):
        assert threading.current_thread() == self
        return self.inq.get(block=block, timeout=timeout)

    def inputs_available(self):
        assert threading.current_thread() == self
        result = []
        try:
            while True:
                result.append(self.inq.get(block=False))
        except queue.Empty:
            pass
        return result

    def send(self, item, block=True, timeout=None):
        assert threading.current_thread() != self
        return self.inq.put(item, block=block, timeout=timeout)

    def receive(self, block=True, timeout=None):
        assert threading.current_thread() != self
        return self.outq.get(block=block, timeout=timeout)

    def receive_available(self):
        assert threading.current_thread() != self
        result = []
        try:
            while True:
                result.append(self.outq.get(block=False))
        except queue.Empty:
            pass
        return result

    @classmethod
    def are_alive(cls, type=None):
        if type is None:
            type = CommonThread
        for thread in threading.enumerate():
            if isinstance(thread, type):
                return True
        return False

    @classmethod
    def join_all(cls, type=None, timeout=None) -> bool:
        t0 = time.time()
        while CommonThread.are_alive(type=type):
            time.sleep(0.0)
            if timeout is not None:
                t1 = time.time()
                if (t1 - t0) >= timeout:
                    return not CommonThread.are_alive(type=type)
        return True

    @classmethod
    def list_alive(cls, type=None):
        if type is None:
            type = CommonThread
        result = []
        for thread in threading.enumerate():
            if isinstance(thread, type):
                result.append(thread)
        return result


class WorkerThread(CommonThread):

    def __init__(self, worker_function, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)
        self.worker_function = worker_function

    def run(self):
        t0 = time.time()
        self.result = self.worker_function(self, *self.args, **self.kwargs)
        t1 = time.time()
        self.elapsed = t1 - t0


class ThreadGroup:

    def __init__(self, *thread_list, auto_start=False):
        self.thread_list = list(thread_list)
        print(self.thread_list)
        self.auto_start = auto_start
        if self.auto_start:
            self.start()

    def start(self):
        for thread in self.thread_list:
            thread.start()

    def is_alive(self):
        for thread in self.thread_list:
            if thread.is_alive():
                return True
        return False

    def join(self, timeout=None):
        t0 = time.time()
        while self.is_alive():
            time.sleep(0.0)
            if timeout is not None:
                t1 = time.time()
                if (t1 - t0) >= timeout:
                    return not self.is_alive()
        return True
