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

def GetCNESnews():
    #取得鉅亨網新聞
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
    import json
    import re
    
    sys.setdefaultencoding='utf8'
    lineArr = []
    
    strresult = ''
    urlToVisit = 'http://news.cnyes.com/news/cat/forex'
    response = requests.get(urlToVisit)
    html = response.content
    #print html
    soup = bs(html,"html.parser")
    ahref = soup.findAll("div", { "class" : "_2nh theme-left-col" })
    a = bs(str(ahref),"html.parser")
    aa = soup.findAll("a",{"class":"_1Zd"})
    for xx in aa:  
        #print xx.text
        #print 'http://news.cnyes.com' + xx['href']
        strresult += xx.text
        strresult += '\n'
        strresult += 'http://news.cnyes.com' + xx['href']
        strresult += '\n'

    return strresult