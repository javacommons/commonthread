from commonthread import *
import datetime
import time


CommonThreadLogger.setup_basic_logging(format='%(threadName)s ==> %(message)s')
lg = CommonThreadLogger()


def worker1(th, *args, **kwargs):
    lg.debug('start')
    lg.debug(args)
    lg.debug(kwargs)
    time.sleep(2)
    lg.debug('end')
    return 1234


def worker3(th, *args):
    lg.debug('start')
    lg.debug(args)
    th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    th.add_argument('x')
    th.add_argument('y')
    th.add_argument('-z', required=True)
    th.add_argument('-w', action='store_true')
    th.add_argument('rest', nargs='*', help='file or directory')
    params = th.parse_args()
    lg.debug('params={}'.format(params))
    time.sleep(2)
    lg.debug('end')


class MyThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args, **kwargs):
        lg.debug('Starting Thread named {}, args={}, kwargs={}'.format(self.name, args, kwargs))
        for i in args:
            lg.debug(i)
        time.sleep(5)
        lg.debug('end')


class ParserThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args):
        self.add_argument('x', type=float)
        self.add_argument('y')
        params = self.parse_args()
        lg.debug('params={}'.format(params))
        time.sleep(4)
        result = 0
        while True:
            inputs = self.inputs_available()
            for i in inputs:
                lg.debug(i)
                if i is None:
                    return result
                else:
                    result += i


lg.debug('starting')

t0 = MyThread('ONE', 'TWO', 'THREE', required=True)
t0.name = 't0@MyThread'
t0.start()

t1 = WorkerThread(worker1, 123, 'abc', 4.56, kw1=1, kw2='abcxyz')
t1.name = "t1@worker1"
t1.start()

t2 = ParserThread(123, datetime.datetime(2017, 9, 1, 12, 12))
t2.name = 't2@ParserThread'
t2.start()

t3 = WorkerThread(worker3, 'install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
t3.name = "t3@worker3"
t3.start()

lg.debug('started')

for i in range(10):
    lg.debug(i)
    t2.send(i)
t2.send(None)

print(CommonThread.some_are_active())

CommonThread.join_all(type=WorkerThread)

print(CommonThread.some_are_active())
print(CommonThread.some_are_active(type=WorkerThread))

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))

CommonThread.join_all()

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))

print(CommonThread.some_are_active())
