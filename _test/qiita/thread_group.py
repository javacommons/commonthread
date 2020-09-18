from commonthread import *


lg = CommonThreadLogger()
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
groupS = ThreadGroup(sth1, sth2); groupS.name='groupS'

lth1 = LongThread(5.0); lth1.name = 'lth1'
lth2 = LongThread(6.0); lth2.name = 'lth2'
groupL = ThreadGroup(lth1, auto_start=True)
groupL.add(lth2)

lg.debug(groupS)
lg.debug(groupL)

groupS.start()
lg.debug(groupS.list_alive())
lg.debug(groupS.list_alive_names())

lg.debug(CommonThread.list_alive_names())

groupS.join()

lg.debug(CommonThread.list_alive_names())

CommonThread.join_all()

lg.debug(CommonThread.list_alive_names())
