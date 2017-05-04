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

line_bot_api = LineBotApi('4VnJ7GkaAtZy8QayMgnZPtTxn+CcgnT7hjdBf8RkBPh/EpttHhf91LIFpukyC2Iiq1m8VacnjZwtwGmIjUV35LK8CPFXU9s7TC5dgK6+DRxinoPbO8SLjrw+1nIgY/q56FULCUZkQIcGVWey212BYQdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('c88afa86017208a7bc6af60be8585a33')



@csrf_exempt
def callback(request):
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
    
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        print body

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        buttons_template = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='服務類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
                actions=[
                    MessageTemplateAction(
                        label='近期上映電影',
                        text='近期上映電影'
                    ),
                    MessageTemplateAction(
                        label='eyny',
                        text='eyny'
                    )
                ]
            )
        )

        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message,TextMessage):
                    print event.reply_token

                    line_bot_api.reply_message(
                        event.reply_token,
                        #TextSendMessage(text=event.message.text),
                        #post_text(event.reply_token,event.message.text)
                        buttons_template
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
