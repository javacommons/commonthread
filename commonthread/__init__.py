import argparse
import logging
import queue
import threading


class CommonThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.args = args
        self.kwargs = kwargs
        self.inq = queue.Queue()
        self.outq = queue.Queue()
        self.parser = argparse.ArgumentParser()
        self.params = None

    def entry(self, *args, **kwargs):
        pass

    def run(self):
        self.entry(*self.args, **self.kwargs)

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
        while not self.inq.empty():
            result.append(self.inq.get())
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
        while not self.outq.empty():
            result.append(self.outq.get())
        return result

    def log_debug(self, msg):
        return logging.debug(msg)

    @classmethod
    def setup_basic_logging(cls, level=logging.DEBUG, format='%(threadName)s: %(message)s'):
        logging.basicConfig(level=level, format=format)

    @classmethod
    def some_are_active(cls):
        for thread in threading.enumerate():
            if isinstance(thread, CommonThread):
                return True
        return False

    @classmethod
    def collect_threads_output(cls):
        result = []
        for thread in threading.enumerate():
            if not isinstance(thread, CommonThread):
                continue
            # while not thread.outq.empty():
            #     result.append(thread.outq.get())
            result.extend(thread.receive_available())
        return result

    @classmethod
    def log_threads_output(cls, use_print=False):
        msg_list = CommonThread.collect_threads_output()
        for msg in msg_list:
            if use_print:
                print(msg)
            else:
                logging.debug(msg)


class WorkerThread(CommonThread):

    def __init__(self, worker_function, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)
        self.worker_function = worker_function

    def run(self):
        self.worker_function(self, *self.args, **self.kwargs)
        return None
