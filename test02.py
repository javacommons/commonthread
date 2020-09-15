from commonthread import *
import time


CommonThreadLogger.setup_basic()
lg = CommonThreadLogger()
lg.debug('hello!')


def worker1(th, x, y):
    lg.debug('start')
    lg.debug('th.name={}'.format(th.name))
    lg.debug('x={}'.format(x))
    lg.debug('y={}'.format(y))
    time.sleep(5)
    lg.debug('end')


t1 = WorkerThread(worker1, 'XXX', 'YYY')
t1.start()
