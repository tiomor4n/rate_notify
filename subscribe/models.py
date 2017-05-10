from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class EmailVerify(models.Model):
    email = models.CharField(max_length=20)
    verify= models.BooleanField(default=False)
    token = models.CharField(max_length=45,default='')
    msgcnt = models.IntegerField(default=0)

class LineInformList(models.Model):
    username = models.CharField(max_length=35,default = '')
    bank = models.CharField(max_length=4)
    BS = models.CharField(max_length=1)
    ccy = models.CharField(max_length=3)
    exrate = models.FloatField(default=0.)
    stoptoday = models.CharField(max_length=1)
    
class comment(models.Model):
    name = models.CharField(max_length=35)
    comments = models.CharField(max_length=200)
    
class oper_para(models.Model):
    name = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    
    

class LineUserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mid = models.CharField(max_length=35)
    token = models.CharField(max_length=45,default='')
    profilesrc= models.CharField(max_length=80,default='')
    msgcnt = models.IntegerField(default=0)
    

'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
            LineUserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.LineUserInfo.save()
'''    
    
'''
https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

'''