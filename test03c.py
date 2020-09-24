from commonthread import *
import time


lg = ThreadLogger()
lg.setup_basic()
lg.debug('hello!')


class MyThread(CommonThread):

    def entry(self, x, y, **kwargs):
        lg.debug('start')
        lg.debug('self.name={}'.format(self.name))
        lg.debug('x={}'.format(x))
        lg.debug('y={}'.format(y))
        lg.debug('kwargs={}'.format(kwargs))
        time.sleep(5)
        lg.debug('end')


t1 = MyThread('XXX', 'YYY', kw1='KeyWord-1')
t1.start()
