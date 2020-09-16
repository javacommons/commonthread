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
        self.args = args
        self.kwargs = kwargs
        self.inq = queue.Queue()
        self.outq = queue.Queue()
        self.parser = argparse.ArgumentParser()
        self.params = None
        self.elapsed = 0.0
        self.result = None

    def entry(self, *args, **kwargs):
        pass

    def run(self):
        t0 = time.time()
        self.result = self.entry(*self.args, **self.kwargs)
        t1 = time.time()
        self.elapsed = t1 - t0

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self):
        str_array = []
        for p in self.args:
            str_array.append(str(p))
        self.params = self.parser.parse_args(str_array)
        return self.params

    def output(self, item, block=True, timeout=None):
        assert threading.current_thread() == self
        return self.outq.put(item, block, timeout)

    def input(self, block=True, timeout=None):
        assert threading.current_thread() == self
        return self.inq.get(block, timeout)

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
        return self.inq.put(item, block, timeout)

    def receive(self, block=True, timeout=None):
        assert threading.current_thread() != self
        return self.outq.get(block, timeout)

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
    def are_active(cls, type=None):
        if type is None:
            type = CommonThread
        for thread in threading.enumerate():
            if isinstance(thread, type):
                return True
        return False

    @classmethod
    def join_all(cls, type=None):
        while CommonThread.are_active(type):
            time.sleep(0.001)
        return None


class WorkerThread(CommonThread):

    def __init__(self, worker_function, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)
        self.worker_function = worker_function

    def run(self):
        t0 = time.time()
        self.result = self.worker_function(self, *self.args, **self.kwargs)
        t1 = time.time()
        self.elapsed = t1 - t0
