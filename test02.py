from commonthread import *
import time


lg = ThreadLogger()
lg.setup_basic()
lg.debug('hello!')


def worker1(th: WorkerThread, x, y):
    lg.debug('start')
    lg.debug('th.name={}'.format(th.name))
    lg.debug('x={}'.format(x))
    lg.debug('y={}'.format(y))
    time.sleep(5)
    lg.debug('end')
    return True


t1 = WorkerThread(worker1, 'XXX', 'YYY')
lg.debug(t1)
t1.start()
t1.join()
lg.debug(t1)
