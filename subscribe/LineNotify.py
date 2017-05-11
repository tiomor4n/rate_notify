# -*- coding: utf8 -*-
import requests
from models import oper_para
from django.contrib.auth.models import User
from models import LineUserInfo


def GetToken(code):
    import json
    client_id = oper_para.objects.get(name='client_id')
    client_secret = oper_para.objects.get(name = 'client_secret')
    redirect_uri = oper_para.objects.get(name = 'redirect_uri')
    print "code:" + code
    print "client_id:" + client_id.content
    print "client_secret:" + client_secret.content
    
    r = requests.post("https://notify-bot.line.me/oauth/token",
                      data={
                          "grant_type":"authorization_code",
                          "code":code,
                          "redirect_uri":redirect_uri.content,
                          "client_id":client_id.content,
                          "client_secret":client_secret.content
                      },
                      headers={
                          "Content-Type":"application/x-www-form-urlencoded"
                      }
                   )
    print r.text
    return r.text
    
def GetLoginToken(code):
    def GetLineProfile(token):
        r = requests.post("https://api.line.me/v2/profile",
                 headers=
                 {
                     "Authorization":"Bearer " + token,
                     "Content-Type":"application/x-www-form-urlencoded"
                 }
            
        )
        print r.text
        return r.text
    
    
    import json
    channel_id = '1512516993'
    client_secret = '2518639a9a3e23e6955276cdef21c99d'
    redirect_uri = 'https://rate-notify-tiomor4n.c9users.io/line_login'
    
    #https://api.line.me/v2/oauth/accesstoken
    r = requests.post("https://api.line.me/v2/oauth/accessToken",
                      data={
                          "grant_type":"authorization_code",
                          "client_id":channel_id,
                          "client_secret":client_secret,
                          "code":code,
                          "redirect_uri":redirect_uri
                      },
                      headers={
                          "Content-Type":"application/x-www-form-urlencoded"
                      }
                   )
    #print r.text
    jsont = json.loads(r.text)
    r=GetLineProfile(jsont['access_token'])
    jsonr = json.loads(r)
    mid = jsonr['userId']
    mName = jsonr['displayName']
    mpictureUrl = jsonr['pictureUrl']
    print 'mid:' + mid
    print 'displayName:' + mName
    print 'pictureUrl:' + mpictureUrl
    return mid, mName, mpictureUrl
    

    
    

def GetLineNotifyUrl(vemail):
    client_id = oper_para.objects.get(name='client_id')
    redirect_uri = oper_para.objects.get(name = 'redirect_uri')
    
    URL = 'https://notify-bot.line.me/oauth/authorize?'
    URL += 'response_type=code'
    URL += '&client_id=' + client_id.content
    URL += '&redirect_uri=' + redirect_uri.content
    URL += '&scope=notify'
    URL += '&state=abcde'
    print URL
    return URL

def sendmsg(vuser= User,msg = ''):
    print "token:" + vuser.lineuserinfo.token
    r = requests.post("https://notify-api.line.me/api/notify",
             data={
                 "message":msg
             },
             headers=
             {
                 "Authorization":"Bearer " + vuser.lineuserinfo.token,
                 "Content-Type":"application/x-www-form-urlencoded"
             }
            
        )
    LU = LineUserInfo.objects.get(user = vuser)
    cnt = LU.msgcnt
    cnt = cnt + 1
    LU.msgcnt = cnt
    LU.token = vuser.lineuserinfo.token
    LU.save()
    print r.text
    return r.text
    
def sendgmail():
    import smtplib
    gu = oper_para.objects.get(name='gu')
    gp = oper_para.objects.get(name='gp')

    gmail_user = gu.content
    gmail_pwd = gp.content
    FROM = 'tiomor4n@gmail.com'
    TO = 'tiomor4n@gmail.com'
    SUBJECT = 'this is subject'
    TEXT = 'text'
    
    message = """
    &lt!DOCTYPE html&gt
    &lthtml&gt
    &lthead&gt
    &lt/head&gt
    &ltbody&gt
    &lttable style='width:60%;margin-left:auto;margin-right:auto;'&gt
    &lttr&gt
    &lttd style='background-color:green;color:#fff;padding-top:50px;padding-bottom:50px;text-align:center;'&gt
    &ltp style='font-size:30px;'&gtThis is sample html email&lt/p&gt
    &lta href='http://www.techipapa.blogspot.com/' style='color:#fff;text-decoration:none;font-size:35px;'&gtClick here&lt/a&gt
    &lt/td&gt
    &lt/tr&gt
    &lt/table&gt
    &lt/body&gt
    &lt/html&gt
    """
    
    

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)         
        print "Successfully sent email"
        return 'mail send'
    except:
        raise
        print "Error: unable to send email"
        return 'mail not send'