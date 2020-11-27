#! python
from commonthread import *
import time

lg = ThreadLogger()
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

    def __init__(self, x, y):
        CommonThread.__init__(self)
        self.setDaemon(True)
        self.params['x'] = x
        self.params['y'] = y

    # def entry(self, x: int, y: int):
    def entry(self):
        lg.debug('start')
        lg.debug('self.name={}'.format(self.name))
        lg.debug('this.params={}')
        time.sleep(5)
        worker = RealWorker(self, self.params['x'], self.params['y'])
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