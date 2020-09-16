from commonthread import *
import time


lg = CommonThreadLogger()
lg.setup_basic()
lg.debug('hello!')


class RealWorker:
    def __init__(self, th: CommonThread, x: int, y: int):
        self.th = th
        self.x = x
        self.y = y

    def calc(self):
        self.th.output('dummy')
        return self.x, self.y


class MyThread(CommonThread):

    def entry(self, x: int, y: int):
        lg.debug('start')
        lg.debug('self.name={}'.format(self.name))
        lg.debug('x={}'.format(x))
        lg.debug('y={}'.format(y))
        time.sleep(5)
        worker = RealWorker(self, x, y)
        result = worker.calc()
        lg.debug('end')
        return result


t1 = MyThread(123, 456)
t1.start()
t1.join()
lg.debug(t1)
a, b = t1.result
lg.debug(a)
lg.debug(b)
c = t1.result
lg.debug(c)
lg.debug(t1.receive_available())