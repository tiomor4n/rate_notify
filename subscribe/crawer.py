# -*- coding: utf8 -*-
def ReadFromStaticBank():
    import json
    from django.conf import settings as djangoSettings
    with open('./' + djangoSettings.STATIC_URL+ '/exrate_' + 'BK'+'.json') as json_data:
        d = json.load(json_data)
    return json.dumps(d,encoding="UTF-8", ensure_ascii=False)
    
def WriteToStatic():
    import json
    import os
    from django.conf import settings as djangoSettings
    from datetime import datetime
    import calendar
    
    tstamp = calendar.timegm(datetime.now().timetuple())
    ccyArr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
        
    jsonBKTW = json.dumps(json.loads(BKTWDataPipe()))
    file = open('./' + djangoSettings.STATIC_URL+ '/exrate_BK.json','w+')
    file.write(jsonBKTW)
    file.close()
    
    
    
def BKTWDataPipe():
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
    import json
    import re
    
    sys.setdefaultencoding='utf8'
    lineArr = []
    
    urlToVisit = 'http://rate.bot.com.tw/xrt?Lang=zh-TW'
    response = requests.get(urlToVisit)
    html = response.content
    soup = bs(html,"html.parser")	
    cashinfo = soup.find('body').findAll('table')[0].findAll('tbody')[0].findAll('tr')
    namedict={u"本行現金買入":"billbuy",
              u"本行現金賣出":"billsell",
              u"本行即期買入":"spotbuy",
              u"本行即期賣出":"spotsell"}
              
    totalObj = {}    
    ccyObj = {}
    ccyObj2 = {}
        
  
    
    for i in range(len(cashinfo)):
        ccyObj2 = {}
        axx = cashinfo[i].findAll('div',{ "class" : "visible-phone print_hide" })       #ccy name
        bxx = cashinfo[i].findAll('td',{ "class" : "rate-content-cash text-right print_hide" })   # billinfo
        cxx = cashinfo[i].findAll('td',{  "class" : "rate-content-sight text-right print_hide" })   # cashinfo
        
        ccyObj2[namedict[bxx[0]['data-table']]] = bxx[0].text.strip()
        ccyObj2[namedict[bxx[1]['data-table']]] = bxx[1].text.strip()
        ccyObj2[namedict[cxx[0]['data-table']]] = cxx[0].text.strip()
        ccyObj2[namedict[cxx[1]['data-table']]] = cxx[1].text.strip()
        
        ccyObj[re.sub(u'[^A-Z]','',axx[0].text.strip())] = ccyObj2
        
    totalObj['BKTW'] = ccyObj
        
    #print json.dumps(totalObj,encoding="UTF-8", ensure_ascii=False)
   
    return json.dumps(totalObj,encoding="UTF-8", ensure_ascii=False)
	
def WriteToStaticBOT(msgstr='',way=''):
    from datetime import datetime
    import calendar
    from django.conf import settings as djangoSettings
    
    msgjson = json.loads(msgstr)
    
    
    mid = mid = msgjson['events'][0]['source']['userId']
    mtext = msgjson['events'][0]['message']['text']
   
        
    
    filename = 'linemsg_' + mid
    tstamp = calendar.timegm(datetime.now().timetuple())
    #確認檔案是否存在
    if os.path.isfile(djangoSettings.STATIC_ROOT + '\\bot\\' + filename):
        #有檔案
        with open(djangoSettings.STATIC_ROOT + '\\bot\linemsg_'+ mid) as msgkeep:
            jdata = json.load(msgkeep)
            print jdata
            stepcnt = jdata['nowstep']
            
        jdata['timestamp'] = tstamp
        talk = jdata['step' + str(stepcnt)]
        if way == 'ask':
            stepcnt = stepcnt + 1
            jdata['step' + str(stepcnt)] = {}
            jdata['step' + str(stepcnt)]['ask'] = mtext
        else:    #reply
            print 'reply'
            talk['reply'] = mtext
                
        jdata['nowstep'] = stepcnt
                
        with open(djangoSettings.STATIC_ROOT + '\\bot\linemsg_'+ mid, 'w+') as msgwrite:
            msgwrite.write(json.dumps(jdata))
            msgwrite.close()
            
    else:
        #沒檔案
        print 'no file'
        step = 0
        msgkeep = {}
        msgkeep['timestamp'] = tstamp
        msgkeep['nowstep'] = step
        msgkeep['step' + str(step)] = {}
        msgkeep['step' + str(step)]['ask'] = mtext
        print msgkeep
        
        file = open(djangoSettings.STATIC_ROOT + '\\bot\linemsg_'+mid , 'w+')
        file.write(json.dumps(msgkeep))
        file.close()

def checkstep(mid=''):
    from django.conf import settings as djangoSettings
    purporse = ''
    step = 0
    filename = djangoSettings.STATIC_ROOT + '\\bot\linemsg_'+ mid
    #先確認檔案是否存在
    if os.path.exists(filename):
        with open(filename) as json_data:
            data= json.loads(json_data)
            step = data['nowstep']
            purporse = data['step0']['ask']
    
    return purporse,step