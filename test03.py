#! python
from commonthread import *
import time

lg = ThreadLogger()
lg.debug('hello!')

def worker1(th, x, y, **kwargs):
    lg.debug('start')
    lg.debug('th.name={}'.format(th.name))
    lg.debug('x={}'.format(x))
    lg.debug('y={}'.format(y))
    lg.debug('kwargs={}'.format(kwargs))
    time.sleep(5)
    lg.debug('end')

t1 = WorkerThread(worker1, 'XXX', 'YYY', kw1='KeyWord-1')
t1.start()
t1.join()
