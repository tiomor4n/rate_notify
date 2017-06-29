# -*- coding: utf8 -*-
from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from subscribe.crawer import ReadFromStaticBank,WriteToStaticBOT,CheckStep,CheckDialog,RemoveDialog
import json
from django.contrib.auth.models import User
from subscribe.models import LineInformList,oper_para
import re

line_bot_api = LineBotApi('4VnJ7GkaAtZy8QayMgnZPtTxn+CcgnT7hjdBf8RkBPh/EpttHhf91LIFpukyC2Iiq1m8VacnjZwtwGmIjUV35LK8CPFXU9s7TC5dgK6+DRxinoPbO8SLjrw+1nIgY/q56FULCUZkQIcGVWey212BYQdB04t89/1O/w1cDnyilFU=')
#parser = WebhookParser('c88afa86017208a7bc6af60be8585a33')
parser = WebhookParser(oper_para.objects.get(name='webhookparser').content)

def CheckUser(mid):
    U = User.objects.filter(username=mid)
    if len(U) == 0:
        return 'no regeist'
    elif U[0].lineuserinfo.token == '':
        return 'no token'
    else:
        return 'ok'
    
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

def GetBSStr(value):
    BSdict = {
        'B':u'買',
        'S':u'賣',
    }
    return BSdict[value]

def GenerateTemplate(kind = '',purporse=''):
    
    
    topicstr = ''
    
    

    if purporse == '/ratecal':
        topicstr =  u'匯率計算機'
    elif purporse == '/ratequote':
        topicstr =  u'匯率報價'
    elif purporse == '/test':
        topicstr =  u'測試用'
    elif purporse == '/ratenotify':
        topicstr = u'會員功能'
        
    

    carousel_template_test = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title=topicstr,
                text=u'請選擇幣別',
                actions=[
                    PostbackTemplateAction(
                        label='postback1',
                        text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message1',
                        text='message text1'
                    ),
                    URITemplateAction(
                        label='uri1',
                        uri='https://rate-notify-tiomor4n.c9users.io/subscribe_bot?move=insert&mid=U131be6da2c9ab40cf71ed6ab972fabcb'
                    )
                ]
            ),
            CarouselColumn(
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackTemplateAction(
                        label='postback2',
                        text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageTemplateAction(
                        label='message2',
                        text='message text2'
                    ),
                    URITemplateAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
    )
    
    #以上是範例
    
    button_template_subtitle = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=topicstr,
                text=u'請選擇功能別',
                actions=[
                    MessageTemplateAction(
                        label=u'訂閱資料管理',
                        text=u'訂閱資料管理'
                    )
                ]
            )
        )

    buttons_template_BS = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=topicstr,
                text='請選擇買賣別',
                actions=[
                    MessageTemplateAction(
                        label=u'買',
                        text=u'買'
                    ),
                    MessageTemplateAction(
                        label=u'賣',
                        text=u'賣'
                    )
                ]
            )
        )
        
    buttons_template_TWDorOTH = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=topicstr,
                text='請問你要',
                actions=[
                    MessageTemplateAction(
                        label=u'台幣換外幣',
                        text=u'台幣換外幣'
                    ),
                    MessageTemplateAction(
                        label=u'外幣換台幣',
                        text=u'外幣換台幣'
                    )
                ]
            )
        )
        
    carousel_template_ccy = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title=topicstr,
                text='請選擇幣別',
                actions=[
                    MessageTemplateAction(
                        label=u'美金',
                        text=u'美金'
                    ),
                    MessageTemplateAction(
                        label=u'人民幣',
                        text=u'人民幣'
                    ),
                    MessageTemplateAction(
                        label=u'港幣',
                        text=u'港幣'
                    )
                ]
            ),
            CarouselColumn(
                title=topicstr,
                text='請選擇幣別',
                actions=[
                    MessageTemplateAction(
                        label=u'歐元',
                        text=u'歐元'
                    ),
                    MessageTemplateAction(
                        label=u'日幣',
                        text=u'日幣'
                    ),
                    MessageTemplateAction(
                        label=u'澳幣',
                        text=u'澳幣'
                    )
                ]
            )
        ]
    )
    )
        
    
    if kind == 'ccy':
        return carousel_template_ccy
    if kind == 'BS':
        return buttons_template_BS
    if kind == 'test':
        return carousel_template_test
    if kind == 'calside':
        return buttons_template_TWDorOTH
    if kind == 'ratenotify':
        return button_template_subtitle


def GenSubscribeTemplate(mid='',purporse = ''):
    s = LineInformList.objects.filter(username = mid)
    llen = len(s)
    aa = oper_para.objects.get(name='hookbackurl')
    
    
    hootbackurl = str(aa.content) + '/subscribe_bot'
    adduri= hootbackurl + '?move=insert&mid=' + mid 
    if llen == 0:
        movearr = [
                URITemplateAction(
                        label=u'新增',
                        uri=adduri
                    )
            ]
        print 'here is lingth 0'
    elif llen == 5:
        movearr = [
                MessageTemplateAction(
                    label=u'修改',
                    text=u'修改'
                ),
                MessageTemplateAction(
                    label=u'刪除',
                    text=u'刪除'
                )
            ]
    else:
        movearr = [
                 URITemplateAction(
                        label=u'新增',
                        uri=adduri
                    ),
                MessageTemplateAction(
                    label=u'修改',
                    text=u'修改'
                ),
                MessageTemplateAction(
                    label=u'刪除',
                    text=u'刪除'
                )
            ]
            
    modifyurlarr=[]
    modifystrarr=[]
    deletearr=[]
    subdataarr1=[]
    subdataarr2=[]
    CCarr = []
    Ccolumn1 = None
    Ccolumn2 = None
    carousel_template_subscribe = None
    print 'length:' + str(len(s))
                
    if len(s) > 0:
        for ss in s:
            strdesc = GetCcyStr(ss.ccy) + '/' + GetBSStr(ss.BS) + '/' + str(ss.exrate)
            modifyGetPara = '?move=update&mid=' + mid + '&id=' + str(ss.id)
            deleteGetPara = 'move=delete&id=' + str(ss.id)
            print 'deleteGetPara:' + deleteGetPara
            modifystrarr.append(strdesc)
            modifyurlarr.append(modifyGetPara)
            deletearr.append(deleteGetPara)
            
    
    if len(s) > 0:
        if len(s) <= 3:
            if len(s) == 1 or len(s) == 2:
                for r in range(0,len(s)):
                    if purporse == 'data':
                        subdataarr1.append(
                                URITemplateAction(
                                     label=modifystrarr[r],
                                     uri=hootbackurl + modifyurlarr[r]
                                )
                            )
                    elif purporse == 'data-del':
                        subdataarr1.append(
                                PostbackTemplateAction(
                                     label=modifystrarr[r],
                                     text=u'已選擇刪除資料',
                                     data=deletearr[r],
                                     
                                )
                            )
                  
            elif len(s) == 3:
                for r in range(0,len(s)):
                    if purporse == 'data':
                        subdataarr1.append(
                                URITemplateAction(
                                     label=modifystrarr[r],
                                     uri=hootbackurl + modifyurlarr[r]
                                )
                            )
                    elif purporse == 'data-del':
                        subdataarr1.append(
                                PostbackTemplateAction(
                                     label=modifystrarr[r],
                                     text=u'已選擇刪除資料',
                                     data=deletearr[r]
                                )
                            )
                   
        elif len(s) == 4:
            print 'len = 4'
            for r1 in range(0,2):
                if purporse == 'data':
                    subdataarr1.append(
                            URITemplateAction(
                                 label=modifystrarr[r1],
                                 uri=hootbackurl + modifyurlarr[r1]
                            )
                        )
                elif purporse == 'data-del':
                    subdataarr1.append(
                           PostbackTemplateAction(
                                     label=modifystrarr[r1],
                                     text=u'已選擇刪除資料',
                                     data=deletearr[r1]
                                )
                        )
                    
            print 'len(subdataarr1):' + str(len(subdataarr1))
             
            for r2 in range(2,len(s)):
                if purporse == 'data':
                    subdataarr2.append(
                            URITemplateAction(
                                 label=modifystrarr[r2],
                                 uri=hootbackurl + modifyurlarr[r2]
                            )
                        )
                elif purporse == 'data-del':
                    subdataarr2.append(
                           PostbackTemplateAction(
                                     label=modifystrarr[r2],
                                     text=u'已選擇刪除資料',
                                     data=deletearr[r2]
                                )
                        )
                
            print 'len(subdataarr2):' + str(len(subdataarr2))
             
           
            
        elif len(s) == 5:
            for r1 in range(0,3):
                if purporse == 'data':
                    subdataarr1.append(
                            URITemplateAction(
                                 label=modifystrarr[r1],
                                 uri=hootbackurl + modifyurlarr[r1]
                            )
                        )
                elif purporse == 'data-del':
                    subdataarr1.append(
                            PostbackTemplateAction(
                                     label=modifystrarr[r1],
                                     text=modifystrarr[r1],
                                     data=deletearr[r1]
                                )
                        )     
            print 'len(subdataarr1):' + str(len(subdataarr1))
                
            for r2 in range(3,len(s)):
                if purporse == 'data':
                    subdataarr2.append(
                            URITemplateAction(
                                    label=modifystrarr[r2],
                                    uri=hootbackurl + modifyurlarr[r2]
                                )
                            )
               
                elif purporse == 'data-del':
                    subdataarr2.append(
                             PostbackTemplateAction(
                                     label=modifystrarr[r2],
                                     text=modifystrarr[r2],
                                     data=deletearr[r2]
                                )
                            )
                
            subdataarr2.append(
                        MessageTemplateAction(
                            label='  ',
                            text='  '
                        )
                    )    
                    
            print 'len(subdataarr2):' + str(len(subdataarr2))
                
                
                    
            print 'CCarr length:' + str(len(CCarr))    
    
        Ccolumn1 = CarouselColumn(
            title=u'請選擇資料',
            text=u'請選擇幣別',
            actions=subdataarr1
            )
        CCarr.append(Ccolumn1)
        
        if len(s) > 3:
            Ccolumn2 = CarouselColumn(
            title=u'請選擇資料',
            text=u'請選擇幣別',
            actions=subdataarr2
            )
            
            CCarr.append(Ccolumn2)
            
        print 'CCarr length:' + str(len(CCarr))   
            
        
        
        carousel_template_subscribe = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=CCarr
            )
        )
    
    buttons_template_subscribedata = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=u'管理訂閱資料',
                text=u'請問你要',
                actions=movearr
            )
        )
        
    if purporse == 'move':
        return buttons_template_subscribedata
    elif purporse in ['data','data-del']:
        print 'data'
        return carousel_template_subscribe
    
                


def RatecalProg(step=0):
    if step == 0:
        return GenerateTemplate('ccy')
    elif step == 1:
        return u'請輸入金額'
    else:
        return 'dialog error'



@csrf_exempt
def callback(request):
    import sys
    sys.setdefaultencoding='utf8'
    def LineMsgOut(mid,message):
        sendmsgstr = '{"events":[{"source":{"userId":"' + mid + '"},"message":{"text":"'+ message + '"}}]}'
        #print sendmsgstr
        WriteToStaticBOT(sendmsgstr,"reply")
        
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


    import json
    import requests
    def post_text(reply_token, text):
        REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 4VnJ7GkaAtZy8QayMgnZPtTxn+CcgnT7hjdBf8RkBPh/EpttHhf91LIFpukyC2Iiq1m8VacnjZwtwGmIjUV35LK8CPFXU9s7TC5dgK6+DRxinoPbO8SLjrw+1nIgY/q56FULCUZkQIcGVWey212BYQdB04t89/1O/w1cDnyilFU="
        }
        payload = {
              "replyToken":reply_token,
              "messages":[
                    {
                        "type":"text",
                        "text": text
                    }
                ]
        }
        requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))
    
    #ccyarr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
    #twayarr = ['BUY','SELL']
    twayarr = [u'買',u'賣']
    ccyarr = [u'港幣',u'美金',u'人民幣',u'歐元',u'澳幣',u'英鎊',u'新加坡幣',u'日幣',u'韓圜']
    actarr = []
    hookbackurl = oper_para.objects.get(name = 'hookbackurl')
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        #print body
        jdata = json.loads(body)
        mid = jdata['events'][0]['source']['userId']
        events = None
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        
        

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message,TextMessage):
                    print event.reply_token
                    #從這邊開始可以確認收到的字串再決定要做甚麼
                    
                    retrate = ''
                    if event.message.text in ccyarr:
                        WriteToStaticBOT(body,"ask")
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        print 'purporse and step:' + purporse + ' ' + str(step)
                        if purporse == '/ratequote' or purporse == u'匯率報價':
                            if CheckDialog(mid):
                                #RemoveDialog(mid)
                                pass
                            
                            jdata = json.loads(ReadFromStaticBank())
                            print 'last ask:' + last_ask
                            if last_ask == u'買':
                                retrate = jdata['BKTW'][GetCcyStrChn(event.message.text)]['spotsell']
                            elif last_ask == u'賣':
                                retrate = jdata['BKTW'][GetCcyStrChn(event.message.text)]['spotbuy']
                            
                            print 'retrate:' + retrate
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=retrate),
                            )
                            LineMsgOut(mid = mid,message = retrate)
                        elif purporse == '/ratecal1' or purporse == u'台幣換外幣':
                            jdata = json.loads(ReadFromStaticBank())
                            print 'last ask:' + last_ask
                            retrate = (float(jdata['BKTW'][GetCcyStrChn(event.message.text)]['spotsell'])  + float(jdata['BKTW'][GetCcyStrChn(event.message.text)]['spotbuy'])) / 2
                            ret = u'新台幣' + last_ask + u'折合'  + event.message.text  + u'為' + str(round(float(last_ask) / retrate,2)) + u'元'
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=ret),
                            )
                            LineMsgOut(mid = mid,message = ret)
                        elif purporse == '/ratecal2' or purporse == u'外幣換台幣':
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=u'請輸入' + event.message.text + u'金額'),
                            )
                            LineMsgOut(mid = mid,message = u'input amount')
                                
                            
                    elif event.message.text == '/ratequote' or event.message.text == u'匯率報價':
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        WriteToStaticBOT(body,"ask")
                        line_bot_api.reply_message(
                            event.reply_token,
                            GenerateTemplate('BS','/ratequote')
                        )
                        LineMsgOut(mid = mid,message = u'input B/S')
                    elif event.message.text in twayarr:
                        WriteToStaticBOT(body,"ask")
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        print 'purporse and step:' + purporse + ' ' + str(step)
                        if purporse == '/ratequote' or purporse == u'匯率報價':
                            line_bot_api.reply_message(
                                event.reply_token,
                                GenerateTemplate('ccy','/ratequote')
                            )
                            LineMsgOut(mid = mid,message = u'input ccy')
                        else:
                            pass
                    elif event.message.text == '/ratecal'  or event.message.text == u'匯率計算機':
                        line_bot_api.reply_message(
                                event.reply_token,
                                GenerateTemplate('calside','/ratecal'),
                            )

                    elif event.message.text == '/ratecal1' or event.message.text == u'台幣換外幣':
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        WriteToStaticBOT(body,"ask")
                        if step == 0:
                            print 'ratecal start'
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=u'請輸入新台幣金額'),
                            )
                            LineMsgOut(mid = mid,message = u'input amount')
                            
                    elif event.message.text == '/ratecal2'  or event.message.text == u'外幣換台幣':
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        WriteToStaticBOT(body,"ask")
                        if step == 0:
                            print 'ratecal start'
                            line_bot_api.reply_message(
                                event.reply_token,
                                GenerateTemplate('ccy','/ratecal'),
                            )
                            LineMsgOut(mid = mid,message = u'input ccy')
                       
                    
                    elif event.message.text == '/aboutme' or event.message.text == u'關於我':
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        WriteToStaticBOT(body,"ask")
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=u'您好，我可以幫你注意最新的匯率報價，並主動通知您。 如果您對我們的服務有想說的話，歡迎到以下連結告訴我們 https://goo.gl/JQS1Bg'),
                        )
                        LineMsgOut(mid = mid,message = u'關於我')
                    
                    #會員功能
                    elif event.message.text == '/ratenotify' or event.message.text == u'會員功能':
                        if CheckUser(mid) == 'ok':
                            WriteToStaticBOT(body,"ask")
                            line_bot_api.reply_message(
                                event.reply_token,
                                GenerateTemplate('ratenotify','/ratenotify')
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=u'您尚未註冊，請點選以下連結開始註冊 ' + GetShortUrl(str(hookbackurl.content) + '/line_login')),
                            )
                            
                    elif event.message.text == u'訂閱資料管理': 
                        line_bot_api.reply_message(
                                event.reply_token,
                                GenSubscribeTemplate(mid,'move')
                            )
                            
                    elif event.message.text == u'修改':     
                        line_bot_api.reply_message(
                                event.reply_token,
                                GenSubscribeTemplate(mid,'data')
                            )
                    elif event.message.text == u'刪除': 
                        if CheckDialog(mid):
                            RemoveDialog(mid)
                        WriteToStaticBOT(body,"ask")
                        line_bot_api.reply_message(
                                event.reply_token,
                                GenSubscribeTemplate(mid,'data-del')
                            )
                        LineMsgOut(mid = mid,message = 'pick delete data')
                    elif event.message.text == u'是':
                        WriteToStaticBOT(body,"ask")
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        print 'purporse:' + purporse
                        if purporse == u'刪除':
                            print 'last ask:' + last_ask
                            pd = LineInformList.objects.filter(id = last_ask).delete()
                        line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=u'已刪除完成')
                            )
                            
                        
                    
                    elif isfloat(event.message.text):
                        WriteToStaticBOT(body,"ask")
                        purporse,step,last_ask,timestamp = CheckStep(mid)
                        print 'purporse and step:' + purporse + ' ' + str(step)
                        if purporse == '/ratecal1' or purporse == u'台幣換外幣':
                            line_bot_api.reply_message(
                                event.reply_token,
                                GenerateTemplate('ccy','/ratecal')
                            )
                            LineMsgOut(mid = mid,message = u'input ccy')
                        if purporse == '/ratecal2' or purporse == u'外幣換台幣':
                            jdata = json.loads(ReadFromStaticBank())
                            retrate = (float(jdata['BKTW'][GetCcyStrChn(last_ask)]['spotsell'])  + float(jdata['BKTW'][GetCcyStrChn(last_ask)]['spotbuy'])) / 2
                            ret = event.message.text + last_ask + u'折合新台幣為' + str(round(float(event.message.text) * retrate,2)) + u'元'
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=ret),
                            )
                            LineMsgOut(mid = mid,message = ret)
                    
                    elif event.message.text == u'已選擇刪除資料':
                        pass
                    
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='我無法判讀您的動作，您可以從下方選單中重新選擇你所要使用的功能'),
                        )
            elif isinstance(event, PostbackEvent):
                print 'postback:' + event.postback.data
                '''
                action=buy&itemid=1
                '''
                m1 = re.search('(?<=move=)\w+',event.postback.data)
                m2 = re.search('(?<=id=)\w+',event.postback.data)
                print m1.group(0)
                print m2.group(0)
                move = m1.group(0)
                sid = m2.group(0)
                sendmsgstr = '{"events":[{"source":{"userId":"' + mid + '"},"message":{"text":"'+ sid + '"}}]}'
                WriteToStaticBOT(sendmsgstr,'ask')
                confirm_template = ConfirmTemplate(text=u'請確定刪除', actions=[
                                     MessageTemplateAction(label=u'是', text=u'是'),
                                     MessageTemplateAction(label=u'否', text=u'否'),
                            
                            ])
                template_message = TemplateSendMessage(
                            alt_text=u'請確定刪除', template=confirm_template)
                line_bot_api.reply_message(
                            event.reply_token,
                            template_message
                        )
                
                
            
            elif isinstance(event,FollowEvent):
                print 'hit follow event'
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
        
'''
http://huli.logdown.com/posts/726082-line-bot-api-tutorial
https://github.com/line
http://www.oxxostudio.tw/articles/201701/line-bot.html
http://lee-w-blog.logdown.com/posts/1134898-line-echo-bot-on-django
https://github.com/Lee-W/line_echobot/blob/master/echobot/views.py
http://blog.masterstudio101.com/2013/05/12/cURL%20%E6%8C%87%E4%BB%A4%E6%95%99%E5%AD%B8%20(cURL%20command%20how-to)
'''
