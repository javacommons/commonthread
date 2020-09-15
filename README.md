# commonthread - Common Threading Library

* What code looks like:

```python:demo.py
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

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))

CommonThread.join_all()

lg.debug('t1.result={}'.format(t1.result))
lg.debug('t2.result={}'.format(t2.result))

print(CommonThread.some_are_active())
```

* Output:

```
C:\root\commonthread\venv\Scripts\python.exe C:/root/commonthread/demo.py
MainThread ==> starting
t0@MyThread ==> Starting Thread named t0@MyThread, args=('ONE', 'TWO', 'THREE'), kwargs={'required': True}
t0@MyThread ==> ONE
t0@MyThread ==> TWO
t0@MyThread ==> THREE
t1@worker1 ==> start
t1@worker1 ==> (123, 'abc', 4.56)
t1@worker1 ==> {'kw1': 1, 'kw2': 'abcxyz'}
t2@ParserThread ==> params=Namespace(x=123.0, y='2017-09-01 12:12:00')
t3@worker3 ==> start
t3@worker3 ==> ('install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
t3@worker3 ==> params=Namespace(operation='install', rest=['123', '456'], w=False, x='abc', y='XYZ', z='78.654321')
MainThread ==> started
MainThread ==> 0
MainThread ==> 1
MainThread ==> 2
MainThread ==> 3
MainThread ==> 4
MainThread ==> 5
MainThread ==> 6
MainThread ==> 7
MainThread ==> 8
MainThread ==> 9
True
t3@worker3 ==> end
t1@worker1 ==> end
MainThread ==> t1.result=1234
MainThread ==> t2.result=None
t2@ParserThread ==> 0
t2@ParserThread ==> 1
t2@ParserThread ==> 2
t2@ParserThread ==> 3
t2@ParserThread ==> 4
t2@ParserThread ==> 5
t2@ParserThread ==> 6
t2@ParserThread ==> 7
t2@ParserThread ==> 8
t2@ParserThread ==> 9
t2@ParserThread ==> None
t0@MyThread ==> end
MainThread ==> t1.result=1234
MainThread ==> t2.result=45
False

Process finished with exit code 0
```
