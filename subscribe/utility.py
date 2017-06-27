# -*- coding: utf8 -*-
def getTimeStamp():
    import calendar
    import datetime
    d = datetime.datetime.now()
    timestamp1 = calendar.timegm(d.timetuple())
    return timestamp1
    
def GetShortUrl(vlongurl):
    import requests
    import urllib
    import json
    from models import oper_para
    
    
    enlongrul = urllib.quote(vlongurl,safe = '')
    #ACCESS_TOKEN = 'c68d130e6955de2191e9889f2ea2f24e9b6cc3e2'
    ACCESS_TOKEN = oper_para.objects.get(name = 'shorturltoken').content
    execurl = 'https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}'.format(ACCESS_TOKEN,enlongrul)
    r = requests.get(execurl)
    js = json.loads(r.content)
    #return json.dumps(js['data']['url'],encoding='UTF-8',ensure_ascii=False)
    return js['data']['url']



    
    
def encryptdan(target):
    from itsdangerous import URLSafeSerializer
    from subscribe.models import oper_para
    secretkey = oper_para.objects.get(name='sk')
    s = URLSafeSerializer(secretkey.content)
    result = s.dumps(target)
    return result 
    
    
def decryptdan(target):
    from itsdangerous import URLSafeSerializer
    from subscribe.models import oper_para
    try:
        secretkey = oper_para.objects.get(name='sk')
        s = URLSafeSerializer(secretkey.content)
        result = s.loads(target)
        return result
    except:
        return 'illegal decrypt'

def GetCcyStr(value):
    ccydict = {
        'HKD':u'港幣',
        'USD':u'美金',
        'CNY':u'人民幣',
        'EUR':u'歐元',
        'AUD':u'澳幣',
        'GBP':u'英鎊',
        'SGD':u'新加坡幣',
        'JPY':u'日幣',
        'KRW':u'韓圜'
    }
    return ccydict[value]
    
def GetCcyStrChn(value):
    ccydict = {
        u'港幣':'HKD',
        u'美金':'USD',
        u'人民幣':'CNY',
        u'歐元':'EUR',
        u'澳幣':'AUD',
        u'英鎊':'GBP',
        u'新加坡幣':'SGD',
        u'日幣':'JPY',
        u'韓圜':'KRW'
    }
    return ccydict[value]