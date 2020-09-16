from commonthread import *


class AddThread(CommonThread):

    def __init__(self, x: int, y: int):
        CommonThread.__init__(self)
        self.x = x
        self.y = y

    def entry(self):
        return self.x + self.y


thread = AddThread(11, 22)
thread.start()
thread.join()
print('result={}'.format(thread.result))
print('elapsed={}'.format(thread.elapsed))
print(thread)
