from commonthread import *


lg = ThreadLogger()
lg.setup_basic()

d = {'kanagawa': ['横浜', '相模原', '湘南', '鎌倉'],
     'saitama': ['所沢',
                 '狭山',
                 '川口',
                 '浦和',
                 '小手指',
                 '飯能'],
     'tokyo': ['品川', '五反田', '三軒茶屋', '四谷']}

lg.debug(d)
lg.debug(d, True)
lg.debug(d, pretty=True)
lg.info(d, True)
lg.info(d, pretty=True)
