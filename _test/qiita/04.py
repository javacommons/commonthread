from commonthread import *


lg = ThreadLogger()
lg.setup_basic()


class ShortThread(CommonThread):

    def entry(self, duration):
        lg.debug('start')
        time.sleep(duration)
        lg.debug('end')
        return 'finished'


class LongThread(CommonThread):

    def entry(self, duration):
        lg.debug('start')
        time.sleep(duration)
        lg.debug('end')
        return 'finished'


lg.debug('start')

sth1 = ShortThread(1.0); sth1.name = 'sth1'
sth2 = ShortThread(1.5); sth2.name = 'sth2'

lth1 = LongThread(5.0); lth1.name = 'lth1'
lth2 = LongThread(6.0); lth2.name = 'lth2'

sth1.start()
sth2.start()
lth1.start()
lth2.start()

lg.debug(CommonThread.list_alive())

CommonThread.join_all(type=ShortThread)

lg.debug(CommonThread.list_alive())

CommonThread.join_all()

lg.debug(CommonThread.list_alive())
