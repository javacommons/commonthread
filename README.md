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
    th.output('from worker1')
    time.sleep(2)
    lg.debug('end')


def worker3(th, *args):
    lg.debug('start')
    lg.debug(args)
    th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    th.add_argument('x')
    th.add_argument('y')
    th.add_argument('-z', required=True)
    th.add_argument('-w', action='store_true')
    th.add_argument('rest', nargs='*', help='file or directory')
    th.parse_args()
    lg.debug(th.params)
    time.sleep(2)
    lg.debug('end')


class MyThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args, **kwargs):
        lg.debug('Starting Thread named {}, args={}, kwargs={}'.format(self.name, args, kwargs))
        self.outq.put(['this', 'is', 'array'])
        lg.debug(self.args)
        for i in self.args:
            lg.debug(i)
            self.output(i)
        time.sleep(5)
        lg.debug('end')


class ParserThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args):
        self.add_argument('x')
        self.add_argument('y')
        # self.add_argument('z')
        self.parse_args()
        lg.debug(self.params)
        while True:
            inputs = self.inputs_available()
            for i in inputs:
                lg.debug(i)
                if i is None:
                    return


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
    print(i)
    t2.send(i)
t2.send(None)

print(CommonThread.some_are_active())
while CommonThread.some_are_active():
    time.sleep(0.001)
    CommonThread.log_threads_output(use_print=True)
CommonThread.log_threads_output(use_print=True)

CommonThread.join_all()

print(CommonThread.some_are_active())
```

* Output:

```
C:\root\commonthread\venv\Scripts\python.exe C:/root/commonthread/demo.py
MainThread ==> starting
t0@MyThread ==> Starting Thread named t0@MyThread, args=('ONE', 'TWO', 'THREE'), kwargs={'required': True}
t0@MyThread ==> ('ONE', 'TWO', 'THREE')
t0@MyThread ==> ONE
t0@MyThread ==> TWO
t0@MyThread ==> THREE
t1@worker1 ==> start
t1@worker1 ==> (123, 'abc', 4.56)
t1@worker1 ==> {'kw1': 1, 'kw2': 'abcxyz'}
t2@ParserThread ==> Namespace(x='123', y='2017-09-01 12:12:00')
t3@worker3 ==> start
t3@worker3 ==> ('install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
t3@worker3 ==> Namespace(operation='install', rest=['123', '456'], w=False, x='abc', y='XYZ', z='78.654321')
MainThread ==> started
t2@ParserThread ==> 0
t2@ParserThread ==> 1
t2@ParserThread ==> 2
0
1
2
3
4
5
t2@ParserThread ==> 3
t2@ParserThread ==> 4
6
7t2@ParserThread ==> 5
t2@ParserThread ==> 6
t2@ParserThread ==> 7

8
9
t2@ParserThread ==> 8
True
['this', 'is', 'array']
ONE
TWO
THREE
from worker1
t2@ParserThread ==> 9
t2@ParserThread ==> None
t1@worker1 ==> end
t3@worker3 ==> end
t0@MyThread ==> end
False

Process finished with exit code 0
```
