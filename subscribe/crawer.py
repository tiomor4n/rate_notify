# -*- coding: utf8 -*-
import os
import json
from django.conf import settings as djangoSettings
from utility import GetCcyStr

#fileroute = djangoSettings.STATIC_ROOT
#prefilename = '\\bot\linemsg_'
fileroute = '.' + djangoSettings.STATIC_URL
prefilename = 'bot/linemsg_'

    

def ReadFromStaticBank():
    #with open('.' + djangoSettings.STATIC_ROOT+ '\\exrate_' + 'BK'+'.json') as json_data:
    with open(djangoSettings.STATIC_ROOT + "\exrate_BK.json") as json_data:
        d = json.load(json_data)
    return json.dumps(d,encoding="UTF-8", ensure_ascii=False)
    
def WriteToStatic():
    from datetime import datetime
    import calendar
    
    tstamp = calendar.timegm(datetime.now().timetuple())
    ccyArr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
        
    jsonBKTW = json.dumps(json.loads(BKTWDataPipe()))
    file = open(djangoSettings.STATIC_ROOT+ '\exrate_BK.json','w+')
    file.write(jsonBKTW)
    file.close()
    
    
    
def BKTWDataPipe():
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
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


def ReadFromStaticBOT(mid):
    import json
    import sys
    sys.setdefaultencoding='utf8'

    filename = prefilename + mid
    filepath = fileroute + filename
    with open(filepath) as json_data:
        d = json.load(json_data)
    return json.dumps(d,encoding="UTF-8", ensure_ascii=False)
    
def WriteToStaticBOT(msgstr='',way=''):
    from datetime import datetime
    import calendar
    import sys
    sys.setdefaultencoding='utf8'
    msgjson = json.loads(msgstr)

    mid = mid = msgjson['events'][0]['source']['userId']
    mtext = msgjson['events'][0]['message']['text']
   
    filename = prefilename + mid
    filepath = fileroute + filename
    tstamp = calendar.timegm(datetime.now().timetuple())
    #確認檔案是否存在
    if os.path.isfile(filepath):
        print u'有檔案'.encode('utf-8')
        with open(filepath) as msgkeep:
            jdata = json.load(msgkeep)
            stepcnt = jdata['nowstep']
            
        jdata['timestamp'] = tstamp
        talk = jdata['step' + str(stepcnt)]
        if way == 'ask':
            
            stepcnt = stepcnt + 1
            jdata['step' + str(stepcnt)] = {}
            jdata['step' + str(stepcnt)]['ask'] = mtext
            print 'ask:' + mtext.encode('utf-8')
        else:    #reply
            talk['reply'] = mtext
            print 'reply:' + mtext.encode('utf-8')
                
        jdata['nowstep'] = stepcnt
                
        with open(filepath, 'w+') as msgwrite:
            msgwrite.write(json.dumps(jdata,encoding="UTF-8", ensure_ascii=False).encode('utf-8'))
            msgwrite.close()
            
    else:
        print u'no file'
        step = 0
        msgkeep = {}
        msgkeep['timestamp'] = tstamp
        msgkeep['nowstep'] = step
        msgkeep['step' + str(step)] = {}
        msgkeep['step' + str(step)]['ask'] = mtext
        print 'ask:' + mtext.encode('utf-8')
        
        file = open(filepath , 'w+')
        file.write(json.dumps(msgkeep))
        file.close()

def CheckStep(mid=''):
    purporse = ''
    step = 0
    last_ask = ''
    timestamp = 0
    
    filename = prefilename + mid
    print filename
    #filepath = './' + djangoSettings.STATIC_URL + '/bot/' + filename
    filepath = fileroute +  filename
    print filepath
    
    #先確認檔案是否存在
    if os.path.exists(filepath):
        with open(filepath) as json_data:
            data= json.load(json_data)
            step = data['nowstep']
            purporse = data['step0']['ask']
            if step == 0:
                last_ask = data['step' + str(step)]['ask']
            else:
                last_ask = data['step' + str(step - 1)]['ask']
            timestamp = data['timestamp']
    
    return purporse,step,last_ask,timestamp

def CheckDialog(mid):
    filepath = fileroute + prefilename + mid
    if os.path.isfile(filepath):
        return True
        

def RemoveDialog(mid):
    filepath = fileroute + prefilename + mid
    os.remove(filepath)
    print 'initial ratecal'
        

