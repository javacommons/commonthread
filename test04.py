from commonthread import *
import time


CommonThreadLogger.setup_basic()
lg = CommonThreadLogger()
lg.debug('hello!')


def worker1(th, x, y, *rest, **kwargs):
    lg.debug('start')
    lg.debug('th.name={}'.format(th.name))
    lg.debug('x={}'.format(x))
    lg.debug('y={}'.format(y))
    lg.debug('rest={}'.format(rest))
    lg.debug('kwargs={}'.format(kwargs))
    time.sleep(5)
    lg.debug('end')


t1 = WorkerThread(worker1, 'XXX', 'YYY', 123, 456, 789, kw1='KeyWord-1')
t1.start()
