# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect
from django.contrib import auth 
from django.contrib.auth.models import User
from subscribe.models import LineInformList,oper_para
from crawer import ReadFromStaticBank,WriteToStatic,BKTWDataPipe
from subscribe.LineNotify import sendmsg,GetToken,GetLoginToken
from subscribe.utility import getTimeStamp,GetShortUrl,encryptdan,decryptdan
#from subscribe.forms import subscribeForm,YourSignupForm,loginForm
import json


def index(request):
    return render_to_response('index.html',locals())
	
def batchOP(vusername):
    
    def genmsgstr(name,ccy,exrate,rate,shortlink):
        msgstr=u'親愛的{},{}已達指定匯率{},現為{},如本日欲停止通知請點選連結{}'.format(name,ccy,exrate,rate,shortlink)
        return msgstr
        
    def getShortUrl(vid):
        from itsdangerous import URLSafeSerializer
        secretkey = oper_para.objects.get(name='sk')
        s = URLSafeSerializer(secretkey.content)
        vid2 = s.dumps(vid)
        shorturl=''
        longurl = 'https://rate-notify-tiomor4n.c9users.io/stoptoday?id={}&TF={}'.format(vid2,'false')    
        print 'longurl:' + longurl
        shorturl = GetShortUrl(longurl)
        return shorturl
    
	
    WriteToStatic()
    '''    
    if vusername == '%':
        AllLine = LineInformList.objects.all()
    else:
        AllLine = LineInformList.objects.filter(username = vusename)
    rateinfo = json.loads(ReadFromStaticBank())
    rateinfob = rateinfo['BKTW']
    result = 'err'
    resultdict = {}
    resultArr = []
    checkmsg= False
    for LL in AllLine:
        resultdict = {}
        if LL.BS == 'B':
            checkpt = 'spotsell'
        else:
            checkpt = 'spotbuy'
        
        strccy = LL.ccy
        strusername = LL.username
        
        if LL.BS == 'B':
            resultdict[strusername] = str(float(rateinfob[strccy][checkpt]) <= LL.exrate)
            checkmsg = float(rateinfob[strccy][checkpt]) <= LL.exrate
            resultdict['rate'] = str(float(rateinfob[strccy][checkpt]))
                
        else:
            resultdict[strusername] = str(float(rateinfob[strccy][checkpt]) > LL.exrate)
            checkmsg = float(rateinfob[strccy][checkpt]) > LL.exrate
            resultdict['rate'] = str(float(rateinfob[strccy][checkpt]))
        
        if checkmsg:
            U = User.objects.get(username = LL.username)
            if LL.stoptoday != 'V':
                shortUrl = getShortUrl(LL.id)
                msgstr = genmsgstr(U.first_name,LL.ccy,LL.exrate,str(float(rateinfob[strccy][checkpt])),shortUrl)
                msgrt = sendmsg(U,msgstr)
                print msgrt
                
        
        resultArr.append(resultdict)
        
    print str(resultArr)
    return json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)
	'''
	
def RunBatchOP(request):
    from django.conf import settings as djangoSettings
    print djangoSettings.STATIC_URL
    print djangoSettings.STATICFILES_DIRS
    batchOP('%')
    return HttpResponse('ok')

