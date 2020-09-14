# commonthread

* What code looks like:

```python:demo.py
from commonthread import *
import datetime
import logging
import time

CommonThread.setup_basic_logging(format='%(threadName)s ==> %(message)s')


def worker1(th, *args, **kwargs):
    th.log_debug('start')
    th.log_debug(args)
    th.log_debug(kwargs)
    th.output('from worker1')
    time.sleep(2)
    th.log_debug('end')


def worker3(th, *args):
    th.log_debug('start')
    th.log_debug(args)
    th.add_argument('operation', choices=['install', 'uninstall', 'update'], help='type of operation')
    th.add_argument('x')
    th.add_argument('y')
    th.add_argument('-z', required=True)
    th.add_argument('-w', action='store_true')
    th.add_argument('rest', nargs='*', help='file or directory')
    th.parse_args()
    th.log_debug(th.params)
    time.sleep(2)
    th.log_debug('end')


class MyThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args, **kwargs):
        self.log_debug('Starting Thread named {}, args={}, kwargs={}'.format(self.name, args, kwargs))
        self.outq.put(['this', 'is', 'array'])
        self.log_debug(self.args)
        for i in self.args:
            self.log_debug(i)
            self.output(i)
        time.sleep(5)
        self.log_debug('end')


class ParserThread(CommonThread):

    def __init__(self, *args, **kwargs):
        CommonThread.__init__(self, *args, **kwargs)

    def entry(self, *args, **kwargs):
        self.add_argument('x')
        self.add_argument('y')
        # self.add_argument('z')
        self.parse_args()
        self.log_debug(self.params)
        while True:
            inputs = self.inputs_available()
            for i in inputs:
                self.log_debug(i)
                if i is None:
                    return


logging.debug('starting')

t0 = MyThread('ONE', 'TWO', 'THREE', required=True)
t0.name = 'MyThread'
t0.start()

t1 = WorkerThread(worker1, 123, 'abc', 4.56, kw1=1, kw2='abcxyz')
t1.name = "worker1"
t1.start()

t2 = ParserThread(123, datetime.datetime(2017, 9, 1, 12, 12))
t2.name = 't2@ParserThread'
t2.start()

t3 = WorkerThread(worker3, 'install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
t3.name = "worker3"
t3.start()

for i in range(30):
    print(i)
    t2.send(i)
t2.send(None)

logging.debug('started')
print(CommonThread.some_are_active())
while CommonThread.some_are_active():
    time.sleep(0.001)
    CommonThread.log_threads_output(use_print=True)
CommonThread.log_threads_output(use_print=True)

print(CommonThread.some_are_active())

```

* Output:

```
C:\root\commonthread\venv\Scripts\python.exe C:/root/commonthread/demo.py
MainThread ==> starting
MyThread ==> Starting Thread named MyThread, args=('ONE', 'TWO', 'THREE'), kwargs={'required': True}
MyThread ==> ('ONE', 'TWO', 'THREE')
MyThread ==> ONE
MyThread ==> TWO
MyThread ==> THREE
worker1 ==> start
worker1 ==> (123, 'abc', 4.56)
worker1 ==> {'kw1': 1, 'kw2': 'abcxyz'}
t2@ParserThread ==> Namespace(x='123', y='2017-09-01 12:12:00')
worker3 ==> start
worker3 ==> ('install', '-z', 78.654321, 'abc', 'XYZ', 123, 456)
worker3 ==> Namespace(operation='install', rest=['123', '456'], w=False, x='abc', y='XYZ', z='78.654321')
t2@ParserThread ==> 0
t2@ParserThread ==> 1
t2@ParserThread ==> 2
t2@ParserThread ==> 3
t2@ParserThread ==> 4
t2@ParserThread ==> 5
t2@ParserThread ==> 6
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
t2@ParserThread ==> 7
t2@ParserThread ==> 8
t2@ParserThread ==> 9
t2@ParserThread ==> 10
t2@ParserThread ==> 11
t2@ParserThread ==> 12
t2@ParserThread ==> 13
t2@ParserThread ==> 14
t2@ParserThread ==> 15
t2@ParserThread ==> 16
t2@ParserThread ==> 17
t2@ParserThread ==> 18
t2@ParserThread ==> 19
t2@ParserThread ==> 20
t2@ParserThread ==> 21
t2@ParserThread ==> 22
t2@ParserThread ==> 23
MainThread ==> started
t2@ParserThread ==> 24
t2@ParserThread ==> 25
t2@ParserThread ==> 26
t2@ParserThread ==> 27
t2@ParserThread ==> 28
t2@ParserThread ==> 29
t2@ParserThread ==> None
21
22
23
24
25
26
27
28
29
True
['this', 'is', 'array']
ONE
TWO
THREE
from worker1
worker1 ==> end
worker3 ==> end
MyThread ==> end
False

Process finished with exit code 0

```
