from commonthread import *
import datetime
import time


lg = CommonThreadLogger()
lg.setup_basic(format='%(threadName)s ==> %(message)s')


# source https://techacademy.jp/magazine/28155
def factorial_worker(th: WorkerThread, n: int):
    if n <= 1:
        return 1
    else:
        return n*factorial_worker(th, n-1)


# source https://techacademy.jp/magazine/28155
def fibonacci_worker(th: WorkerThread, n: int):
    if n <= 2:
        return 1
    else:
        return fibonacci_worker(th, n - 2) + fibonacci_worker(th, n - 1)


class FibonacciThread(CommonThread):

    def entry(self, n: int):
        if n <= 2:
            return 1
        else:
            return self.entry(n - 2) + self.entry(n - 1)


def worker1(th: WorkerThread, *args, **kwargs):
    lg.debug('start')
    lg.debug(args)
    lg.debug(kwargs)
    th.params["abc"] = 1.23
    time.sleep(2)
    lg.debug('end')
    return 1234


def worker3(th: WorkerThread, *args):
    lg.debug('start')
    lg.debug(args)
    th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    th.add_argument('x')
    th.add_argument('y')
    th.add_argument('-z', required=True)
    th.add_argument('-w', action='store_true')
    th.add_argument('rest', nargs='*', help='file or directory')
    th.params = th.parse_args()
    lg.debug('params={}'.format(th.params))
    time.sleep(2)
    lg.debug('end')


class MyThread(CommonThread):

    def entry(self, *args, **kwargs):
        lg.debug('Starting Thread named {}, args={}, kwargs={}'.format(self.name, args, kwargs))
        for i in args:
            lg.debug(i)
        time.sleep(5)
        lg.debug('end')


class ParserThread(CommonThread):

    def entry(self, *args):
        self.add_argument('x', type=float)
        self.add_argument('y')
        params = self.parse_args()
        lg.debug('params={}'.format(params))
        result = 0
        while True:
            inputs = self.inputs_available()
            if inputs:
                lg.debug(inputs)
            for i in inputs:
                lg.debug(i)
                if i is None:
                    return result
                else:
                    result += i


lg.debug('starting')

tfac = WorkerThread(factorial_worker, 6)
tfac.name = 'tfac'
tfac.start()
CommonThread.join_all()
lg.debug('tfac.result={}'.format(tfac.result))

tfib = WorkerThread(fibonacci_worker, 36)
tfib.name = 'tfib'
tfib.start()
CommonThread.join_all()
lg.debug('tfib.result={}'.format(tfib.result))
lg.debug('tfib.elapsed={}'.format(tfib.elapsed))

tfib2 = FibonacciThread(36)
tfib2.name = 'tfib2'
tfib2.start()
CommonThread.join_all()
lg.debug('tfib2.result={}'.format(tfib2.result))
lg.debug('tfib2.elapsed={}'.format(tfib2.elapsed))

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
    time.sleep(0.1)
    lg.debug(i)
    t2.send(i)
t2.send(None)

print(CommonThread.are_active())

CommonThread.join_all(type=WorkerThread)

print(CommonThread.are_active())
print(CommonThread.are_active(type=WorkerThread))

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))

CommonThread.join_all()

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))


lg.debug(tfac)
lg.debug(tfib)
lg.debug(tfib2)
lg.debug(t0)
lg.debug(t1)
lg.debug(t2)
lg.debug(t3)

print(CommonThread.are_active())
