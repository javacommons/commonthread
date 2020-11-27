#! python
from commonthread import *
import time


lg = ThreadLogger()
lg.debug('hello!')


class MyThread(CommonThread):

    def entry(self, x, y, *rest, **kwargs):
        lg.debug('start')
        lg.debug('self.name={}'.format(self.name))
        lg.debug('x={}'.format(x))
        lg.debug('y={}'.format(y))
        lg.debug('rest={}'.format(rest))
        lg.debug('kwargs={}'.format(kwargs))
        time.sleep(5)
        lg.debug('end')


t1 = MyThread('XXX', 'YYY', 123, 456, 789, kw1='KeyWord-1')
t1.start()
