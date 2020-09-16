# commonthread - Common Threading Library

* What code looks like:

```python:demo.py
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

    def entry(self, *args, required=False):
        lg.debug('Starting Thread named {}, args={}, required={}'.format(self.name, args, required))
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
print(CommonThread.list_active())

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
print(CommonThread.list_active())
```

* Output:

```
C:\root\commonthread\venv\Scripts\python.exe C:/root/commonthread/demo.py
MainThread ==> starting
MainThread ==> tfac.result=720
MainThread ==> tfib.result=14930352
MainThread ==> tfib.elapsed=3.5365500450134277
MainThread ==> tfib2.result=14930352
MainThread ==> tfib2.elapsed=4.415233850479126
t0@MyThread ==> Starting Thread named t0@MyThread, args=('ONE', 'TWO', 'THREE'), required=True
t0@MyThread ==> ONE
t0@MyThread ==> TWO
t0@MyThread ==> THREE
t1@worker1 ==> start
t1@worker1 ==> (123, 'abc', 4.56)
t1@worker1 ==> {'kw1': 1, 'kw2': 'abcxyz'}
t2@ParserThread ==> params={'x': 123.0, 'y': '2017-09-01 12:12:00'}
t3@worker3 ==> start
t3@worker3 ==> ('install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
t3@worker3 ==> params={'operation': 'install', 'x': 'abc', 'y': 'XYZ', 'z': '78.654321', 'w': False, 'rest': ['123', '456']}
MainThread ==> started
MainThread ==> 0
t2@ParserThread ==> [0]
t2@ParserThread ==> 0
MainThread ==> 1
t2@ParserThread ==> [1]
t2@ParserThread ==> 1
MainThread ==> 2
t2@ParserThread ==> [2]
t2@ParserThread ==> 2
MainThread ==> 3
t2@ParserThread ==> [3]
t2@ParserThread ==> 3
MainThread ==> 4
t2@ParserThread ==> [4]
t2@ParserThread ==> 4
MainThread ==> 5
t2@ParserThread ==> [5]
t2@ParserThread ==> 5
MainThread ==> 6
t2@ParserThread ==> [6]
t2@ParserThread ==> 6
MainThread ==> 7
t2@ParserThread ==> [7]
t2@ParserThread ==> 7
MainThread ==> 8
t2@ParserThread ==> [8]
t2@ParserThread ==> 8
MainThread ==> 9
t2@ParserThread ==> [9, None]
t2@ParserThread ==> 9
t2@ParserThread ==> None
True
t1@worker1 ==> end
t3@worker3 ==> end
MainThread ==> t1.result=1234
MainThread ==> t2.result=45
True
False
[MyThread(name=t0@MyThread, result=None, elapsed=0.0, args=('ONE', 'TWO', 'THREE'), kwargs={'required': True}, params={})]
t0@MyThread ==> end
MainThread ==> t1.result=1234
MainThread ==> t2.result=45
MainThread ==> WorkerThread(name=tfac, result=720, elapsed=0.0, args=(6,), kwargs={}, params={})
MainThread ==> WorkerThread(name=tfib, result=14930352, elapsed=3.5365500450134277, args=(36,), kwargs={}, params={})
MainThread ==> FibonacciThread(name=tfib2, result=14930352, elapsed=4.415233850479126, args=(36,), kwargs={}, params={})
MainThread ==> MyThread(name=t0@MyThread, result=None, elapsed=5.009608030319214, args=('ONE', 'TWO', 'THREE'), kwargs={'required': True}, params={})
MainThread ==> WorkerThread(name=t1@worker1, result=1234, elapsed=2.010605573654175, args=(123, 'abc', 4.56), kwargs={'kw1': 1, 'kw2': 'abcxyz'}, params={'abc': 1.23})
MainThread ==> ParserThread(name=t2@ParserThread, result=45, elapsed=1.3893027305603027, args=(123, datetime.datetime(2017, 9, 1, 12, 12)), kwargs={}, params={'x': 123.0, 'y': '2017-09-01 12:12:00'})
MainThread ==> WorkerThread(name=t3@worker3, result=None, elapsed=2.0086007118225098, args=('install', '-z', 78.654321, 'abc', 'XYZ', 123, 456), kwargs={}, params={'operation': 'install', 'x': 'abc', 'y': 'XYZ', 'z': '78.654321', 'w': False, 'rest': ['123', '456']})
False
[]

Process finished with exit code 0
```
