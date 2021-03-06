from commonthread import *


# source https://techacademy.jp/magazine/28155
def fibonacci_worker(th: WorkerThread, n: int):
    if n <= 2:
        return 1
    else:
        return fibonacci_worker(th, n - 2) + fibonacci_worker(th, n - 1)


thread = WorkerThread(fibonacci_worker, 36)
thread.name = 'tfib'
thread.start()
success = thread.join(timeout=0.5)
print('success={}'.format(success))
success = thread.join()
print('success={}'.format(success))
print('result={}'.format(thread.result))
print('elapsed={}'.format(thread.elapsed))
print(thread)
