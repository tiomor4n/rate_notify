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
from subscribe.crawer import ReadFromStaticBank,WriteToStaticBOT,checkstep
import json

line_bot_api = LineBotApi('4VnJ7GkaAtZy8QayMgnZPtTxn+CcgnT7hjdBf8RkBPh/EpttHhf91LIFpukyC2Iiq1m8VacnjZwtwGmIjUV35LK8CPFXU9s7TC5dgK6+DRxinoPbO8SLjrw+1nIgY/q56FULCUZkQIcGVWey212BYQdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('c88afa86017208a7bc6af60be8585a33')



@csrf_exempt
def callback(request):
    def LineMsgOut(mid,message):
        sendmsgstr = '{"events":[{"source":{"userId":"' + mid + '"},"message":{"text":"'+ message + '"}}]}'
        print sendmsgstr
        WriteToStaticBOT(sendmsgstr,"reply")


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
    
    ccyarr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
    #ccytextarr = [u'港幣',u'美金',u'人民幣',u'歐元',u'澳幣',u'英鎊',u'新加坡幣',u'日幣',u'韓圜']
    ccytextarr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
    '''
    actarr = [
                    MessageTemplateAction(
                        label='USD',
                        text='USD'
                    ),
                    MessageTemplateAction(
                        label='CNY',
                        text='CNY'
                    )
                ]
    '''
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='this is menu1',
                text='description1',
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
                        uri='http://example.com/1'
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
    actarr = []
    for x in range(0,3):
        actarr.append(MessageTemplateAction(label=ccyarr[x],text=ccytextarr[x]))
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        print body
        jdata = json.loads(body)
        mid = jdata['events'][0]['source']['userId']
        WriteToStaticBOT(body,"ask")
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        '''
        for x in range(0,len(ccyarr)-1):
            actarr.append(MessageTemplateAction(label=ccytextarr[x],text = ccyarr[x]))
        '''
        buttons_template_ccy = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='幣別',
                text='請選擇',
                actions=[
                    MessageTemplateAction(
                        label='USD',
                        text='USD'
                    ),
                    MessageTemplateAction(
                        label='CNY',
                        text='CNY'
                    )
                ]
            )
        )
		
        '''
        buttons_template_ratecal = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='匯率計算機',
                text='請選擇幣別',
                actions=[
                    MessageTemplateAction(
                        label='美金',
                        text='USD'
                    ),
                    MessageTemplateAction(
                        label='人民幣',
                        text='CNY'
                    )
                ]
            )
        )
        '''
        buttons_template_ratecal = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='匯率計算機',
                text='請選擇幣別',
                actions=actarr
            )
        )

        buttons_template_ratereport = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='匯率報價',
                text='請選擇買賣別',
                actions=[
                    MessageTemplateAction(
                        label='買',
                        text='BUY'
                    ),
                    MessageTemplateAction(
                        label='賣',
                        text='SELL'
                    )
                ]
            )
        )
        '''
        buttons_template_ratereport_ccy = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='匯率報價',
                text='請選擇幣別',
                actions=[
                    MessageTemplateAction(
                        label='美金',
                        text='REPORT_USD'
                    ),
                    MessageTemplateAction(
                        label='CNY',
                        text='REPORT_CNY'
                    )
                ]
            )
        )
        '''
        buttons_template_ratereport_ccy = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='匯率報價',
                text='請選擇幣別',
                actions=actarr
            )
        )
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message,TextMessage):
                    print event.reply_token
                    #從這邊開始可以確認收到的字串再決定要做甚麼
                    ccyarr = ['USD','CNY']
                    report_ccy_arr = ['REPORT_USD','REPORT_CNY']
                    twayarr = ['BUY','SELL']
                    if event.message.text in ccyarr:
                        purporse,step = checkstep()
                        print 'purporse and step:' + purporse + ' ' + str(step)
                        jdata = json.loads(ReadFromStaticBank())
                        retrate = jdata['BKTW'][event.message.text]['spotbuy']
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=retrate),
                        )
                        LineMsgOut(mid = mid,message = retrate)
                    elif event.message.text == '/ratecal':
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入金額'),
                        )
                        LineMsgOut(mid = mid,message = '請輸入金額')
                    elif event.message.text == '/ratereport':
                        line_bot_api.reply_message(
                            event.reply_token,
                            buttons_template_ratereport
                        )
                        LineMsgOut(mid = mid,message = '請輸入買賣別')
                    elif event.message.text in twayarr:
                        line_bot_api.reply_message(
                            event.reply_token,
                            #buttons_template_ratereport_ccy
                            carousel_template_message
                        )
                        LineMsgOut(mid = mid,message = '請輸入買賣別')

                    elif isinstance(event.message.text,float):
                        purporse,step = checkstep()
                        print 'purporse and step:' + purporse + ' ' + str(step)
                        #if purporse == '/ratecal':


                        pass


                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='我看不懂你說甚麼'),
                        )
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
        
      


'''
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

def post_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {ENTER_ACCESS_TOKEN}"
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
'''

'''
# Create your views here.
class callback(generic.View):
    
    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        
        token = '4VnJ7GkaAtZy8QayMgnZPtTxn+CcgnT7hjdBf8RkBPh/EpttHhf91LIFpukyC2Iiq1m8VacnjZwtwGmIjUV35LK8CPFXU9s7TC5dgK6+DRxinoPbO8SLjrw+1nIgY/q56FULCUZkQIcGVWey212BYQdB04t89/1O/w1cDnyilFU='
        sevret = 'c88afa86017208a7bc6af60be8585a33'
        line_bot_api = LineBotApi(token)
        parser = WebhookParser('c88afa86017208a7bc6af60be8585a33')
        
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
        
    def get(self, request, *args, **kwargs):
        return HttpResponse('get')
'''


'''
http://huli.logdown.com/posts/726082-line-bot-api-tutorial
https://github.com/line
http://www.oxxostudio.tw/articles/201701/line-bot.html
http://lee-w-blog.logdown.com/posts/1134898-line-echo-bot-on-django
https://github.com/Lee-W/line_echobot/blob/master/echobot/views.py
http://blog.masterstudio101.com/2013/05/12/cURL%20%E6%8C%87%E4%BB%A4%E6%95%99%E5%AD%B8%20(cURL%20command%20how-to)


name:client_id
content:nch5lTjwJmgdHwx5Ar4oaJ
name:client_secret
content:8S6f5tHE1HqE9he2sJW5CrZbHCMn6NbMZadr291111q
name:redirect_uri
content:https://rate-notify-tiomor4n.c9users.io/gettokenfromcode
name:gu
content:tiomor4n@gmail.com
name:gp
content:Aa92351009
name:sk
content:simon


'''
