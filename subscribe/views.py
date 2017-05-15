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
from subscribe.forms import subscribeForm
import json
from django.views.decorators.csrf import csrf_exempt  


def findCCY(vccy):
    ccydict = {
        'HKD':u'港幣',
        'USD':u'美金',
        'CNY':u'人民幣',
        'EUR':u'歐元',
        'AUD':u'澳幣',
        'GBP':u'英鎊',
        'SGD':u'新加坡幣',
        'JPY':u'日幣',
        'KRW':u'韓圜',
        'DEL':u'刪除',
        'INT':u'請輸入'
    }
    return ccydict[vccy]
	
	
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



def RunBatchOP(request):
    from django.conf import settings as djangoSettings
    print djangoSettings.STATIC_URL
    print djangoSettings.STATICFILES_DIRS
    batchOP('%')
    return HttpResponse('ok')
    
def checkOP(vusername):
    import sys
    reload (sys)
    sys.setdefaultencoding('utf-8')
    AllLine = LineInformList.objects.filter(username = vusername)
    #EV = EmailVerify.objects.get(email = vemail)
    U  = User.objects.get(username = vusername)
    msgstr = str('親愛的{},您的訂閱資訊為').format(U.first_name)
    print msgstr
    msgstr2 = u''
    BSdict = {
        'B':u'買',
        'S':u'賣',
        }
        
    for L in AllLine:
        print L.username
        Lccy = findCCY(L.ccy)
        Lexrate = L.exrate
        LBS = BSdict[L.BS]
        msgstr2 = '幣別:' + Lccy.encode('utf-8') + ',買賣別:' + LBS.encode('utf-8') + ',匯率' + str(Lexrate).encode('utf-8') +';'
        msgstr = msgstr + msgstr2
    
        
    msgrt = sendmsg(U,msgstr)
    print msgrt

def subsummary(request):
    from itsdangerous import URLSafeSerializer
    if request.user.is_authenticated():
        secretkey = oper_para.objects.get(name='sk')
        s = URLSafeSerializer(secretkey.content)
        uname = request.user.username
        ldata = LineInformList.objects.filter(username = request.user.username)
        print len(ldata)
        
        if len(ldata) > 0:
            for l in ldata:
                l.id = s.dumps(l.id)
                l.ccy = findCCY(l.ccy)
                if l.BS == 'B':
                    l.BS = u'買'
                else:
                    l.BS = u'賣'
        
    return render_to_response('subsummary.html',locals())

@csrf_exempt
def subscribe(request):
    from itsdangerous import URLSafeSerializer
    
    if request.user.is_authenticated():
        
        if request.method == 'POST':
            showerr = 'X'
            vmove = request.POST['move']
            print 'add/modified data finish'
            #資料輸入完成後回來處理
            vccy = request.POST['ccy']
            vBS = request.POST['BS']
            vexrate = request.POST['exrate']
            vid = request.POST['id']
            errors=[]
            
            vtoken = request.user.lineuserinfo.token
            f = subscribeForm({'BS':vBS,'ccy':vccy,'exrate':vexrate})
            print 'BS:' + vBS
            print 'ccy:' + vccy
            print 'exrate:' + vexrate
            print f.is_valid()    
            print vmove
            if f.is_valid():
                if vmove == 'N':
                #新增資料    
                    Line1 = LineInformList(username = request.user.username,
                        bank = 'BKTW',
                        BS = vBS,
                        ccy = vccy,
                        exrate = vexrate,
                        stoptoday = 'X'
                        )
                    Line1.save()
                    return HttpResponseRedirect('/subsummary/')
                    #return render_to_response('subsummary.html',RequestContext(request,locals()))
                else:
                #修改資料
                    vid = request.POST['id']
                    Line1 = LineInformList.objects.get(id = vid)
                    Line1.BS = vBS
                    Line1.ccy = vccy
                    Line1.exrate = vexrate
                    Line1.save()
                    return HttpResponseRedirect('/subsummary/')
                    #return render_to_response('subsummary.html',RequestContext(request,locals()))
            else:
                showerr = 'V'
                print f['BS'].errors
                print f['ccy'].errors
                print f['exrate'].errors
                #singleL = LineInformList.objects.get(id = request.POST['id'])
                #return render_to_response('subscribe.html',RequestContext(request,locals()))
                return render_to_response('subscribe.html',locals())
                    
                
        #修改資料
        if request.method == 'GET': 
            showerr = 'X'
            if 'id' in request.GET and request.GET['id'] != '':
                try:
                    secretkey = oper_para.objects.get(name='sk')
                    s = URLSafeSerializer(secretkey.content)
                    vid = s.loads(request.GET['id'])
                except:
                    #違法進入，回首頁
                    return HttpResponseRedirect('/')
            
                print 'going to modifiy data'    
                singleL = LineInformList.objects.get(id = vid)
                vmove = 'U'
                f = subscribeForm(initial={'BS':singleL.BS,'ccy':singleL.ccy,'exrate':singleL.exrate})
                return render_to_response('subscribe.html',locals())
            else:
                #第一次出現此頁面
                print 'first time show'
                f = subscribeForm(initial={'BS':'I','ccy':'INT','exrate':''})
                vmove = 'N'
                #print f
                return render_to_response('subscribe.html',locals())
                
    else:
        #違法進入，回首頁
        return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    return render_to_response('index.html',locals()) 

def stoptoday(request):
    import sys
    from itsdangerous import URLSafeSerializer
    try:
        if 'id' in request.GET and request.GET['id'] != '':
            try:
                secretkey = oper_para.objects.get(name='sk')
                s = URLSafeSerializer(secretkey.content)
                vid = s.loads(request.GET['id'])
            except:
                return HttpResponseRedirect('/')
            
            #singleL = LineInformList.objects.get(id = request.GET['id'])
            singleL = LineInformList.objects.get(id = vid)
            print 'id:' + str(request.GET['id'])
            print 'TF:' + str(request.GET['TF'])
            if request.GET['TF'] == 'true':
                singleL.stoptoday = 'X'
            else:
                singleL.stoptoday = 'V'
            singleL.save()
            return HttpResponse('您好，本通知本日已停用')
    except ValueError:
        pass

def GetLineNotify(request):
    from LineNotify import GetLineNotifyUrl
    if request.user.is_authenticated(): 
        uemail = request.user.email
    else:
        uemail = request.GET['email']
    print uemail
    
    URL = GetLineNotifyUrl(uemail)
    return redirect(URL)    
    
        
def GetTokenFromCode(request):
    #uemail = request.GET['state']
    from models import LineUserInfo
    
    mid = request.user.username
    
    strcode = request.GET['code']
    reply = GetToken(strcode)
    print 'reply:' + reply
    if reply != '':
        print 'okok'
        
        replyjs = json.loads(reply)
        tokenstr = replyjs['access_token']
        print 'tokenstr:' + tokenstr
        
        LU = LineUserInfo.objects.get(user = request.user)
        LU.token = tokenstr
        LU.save()
        
        sendmsg(request.user,'你好，歡迎使用RateNotify服務')
        
    return render_to_response('GetTokenFromCode.html') 

def getnotifyinfo(request):
    vusername = request.GET['username']
    checkOP(vusername)
    return HttpResponse('correct')

def hist_data(request):
    return render_to_response('hist_data.html')
    
def line_login(request):
    
    def deal_login_data(mid='',mName='',mpictureUrl=''):
        import random
        from .models import LineUserInfo
        a = random.sample(range(0, 999999), 1)
        randpw = 'ttttt' + str(a[0])
        print randpw
        targetuser = User.objects.filter(username = mid)
        if len(targetuser) > 0:
            print len(targetuser)
            print 'user found'
            #有這個使用者，重設密碼後登入
            targetuser[0].set_password(randpw)
            targetuser[0].lineuserinfo.mid = mid
            targetuser[0].first_name = mName
            targetuser[0].lineuserinfo.profilesrc = mpictureUrl
            targetuser[0].save()
            targetuser[0].lineuserinfo.save()
            
            user = auth.authenticate(username=mid, password=randpw)
            if user is not None and user.is_active:
                auth.login(request, user)
                return 'Line Login success'
        else:
            #新使用者，要註冊
            print 'new user regist'
            new_user = User.objects.create_user(username=mid,password=randpw,first_name=mName)
            new_user.save()
            LU = LineUserInfo(user = new_user,
                               mid = mid,
                               profilesrc = mpictureUrl)
            LU.save()
            user = auth.authenticate(username=mid, password=randpw)
            auth.login(request,user)
            #Line Notify連結
            print 'Line regeist success'
            return 'Line regeist success'
        
    if request.method == 'GET' and 'code' in request.GET:
        print request.GET['code']
        code = request.GET['code']
        mid,mName ,mpictureUrl = GetLoginToken(code)
        rr = deal_login_data(mid,mName,mpictureUrl)
        print rr
        if rr == 'Line regeist success':
            return render_to_response('register_ok.html')
        else:
            return HttpResponseRedirect('/subsummary/')
        
    else:
        URL = 'https://access.line.me/dialog/oauth/weblogin?'
        URL += 'response_type=code&client_id=1512516993'
        URL += '&redirect_uri=https://stark-refuge-18608.herokuapp.com/line_login&state=12345'
        return redirect(URL)
        #return render_to_response('Line_Login.html') 