# -*- coding: utf8 -*-
from subscribe.utility import getTimeStamp
from subscribe.crawer import ReadFromStaticBank
import json
from django.conf import settings as djangoSettings
    
def WriteToStatic():
    from datetime import datetime
    import calendar
    
    tstamp = calendar.timegm(datetime.now().timetuple())
    ccyArr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
        
    #jsonBKTW = json.dumps(json.loads(BKTWDataPipe()))
    file = open('./' + djangoSettings.STATIC_URL+ '/exrate_BK.json','w')
    #file.write(jsonBKTW)
    file.close()