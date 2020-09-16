from commonthread import *
import time


lg = CommonThreadLogger()
lg.setup_basic()
lg.debug('hello!')


class MyThread(CommonThread):
    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)
    def entry(self, x, y):
        lg.debug('start')
        lg.debug('self.name={}'.format(self.name))
        lg.debug('x={}'.format(x))
        lg.debug('y={}'.format(y))
        time.sleep(5)
        lg.debug('end')


t1 = MyThread('XXX', 'YYY')
t1.start()
