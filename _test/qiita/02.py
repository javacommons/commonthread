from commonthread import *


# source https://techacademy.jp/magazine/28155
class FibonacciThread(CommonThread):

    def entry(self, n: int):
        if n <= 2:
            return 1
        else:
            return self.entry(n - 2) + self.entry(n - 1)


thread = FibonacciThread(36)
thread.name = 'tfib'
thread.start()
thread.join()
print('result={}'.format(thread.result))
print('elapsed={}'.format(thread.elapsed))
print(thread)
