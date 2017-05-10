# -*- coding: utf8 -*-
from django import forms
from subscribe.models import LineInformList
import re
from django.contrib.auth.forms import UserCreationForm
#from allauth.account.forms import LoginForm,SignupForm
from django.contrib import auth 


'''
class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['login'].widget = forms.TextInput(attrs={'class':'form-control'})
'''   
    
            

'''
class YourSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(YourSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
'''        


class subscribeForm(forms.Form):
    #BS = forms.CharField(max_length=1,required=True,label =u'買/賣別',widget=forms.TextInput(attrs={'class':'form-control'}) )
    BSlist = (('B',u'買'),('S',u'賣'),('I','-'))
    ccylist = (
        ('INT',u'請輸入'),
        ('DEL',u'刪除'),
        ('HKD',u'港幣'),
        ('USD',u'美金'),
        ('CNY',u'人民幣'),
        ('EUR',u'歐元'),
        ('AUD',u'澳幣'),
        ('GBP',u'英鎊'),
        ('SGD',u'新加坡幣'),
        ('JPY',u'日幣'),
        ('KRW',u'韓圜'))
    BS = forms.ChoiceField(choices=BSlist,label=u'買/賣別',widget=forms.Select(attrs={'class':'form-control'}))
    ccy = forms.ChoiceField(choices=ccylist,label=u'幣別',widget=forms.Select(attrs={'class':'form-control'}))
    exrate = forms.CharField(max_length=8,required=True,label = u'目標匯率',widget=forms.TextInput(attrs={'class':'form-control',
         'placeholder':u'請輸入'
    }))
    
    def clean_exrate(self):
        exrate = self.cleaned_data['exrate']
        print type(exrate)
        try:
            intexrate = float(exrate)
        except ValueError:
            raise forms.ValidationError(u'請輸入數字')
            
        return self.cleaned_data['exrate']
       

class loginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'class':'form-control',
        'id':'email',
        'name':'email',
        'placeholder':'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'id':'password',
        'name':'password'
    }))
        
        
    def clean_password(self):
        print 'err valid'
        vusername = self.cleaned_data['username']
        vpassword = self.cleaned_data['password']
        user = auth.authenticate(username=vusername, password=vpassword)
        if user is None:
            raise forms.ValidationError(u'您輸入的帳號/密碼有誤')
        return self.cleaned_data['email']
    
    
class resetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=30,required=True,label =u'請輸入密碼')
    password2 = forms.CharField(max_length=30,required=True,label =u'請再輸入一次密碼')
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 != password2:
            raise forms.ValidationError(u'須輸入相同密碼')
            
        return self.cleaned_data['password2']

