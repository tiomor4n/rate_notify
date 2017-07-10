from django.conf.urls import include, url
from django.contrib import admin
from subscribe.views import index
from subscribe.views import RunBatchOP,line_login,GetLineNotify,GetTokenFromCode,subscribe_bot,writeDB_bot
from subscribe.views import writeDB_bot2,stoptoday,RunBatchnonstop,RunBatchGetRate

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', index),
	url(r'^line_bot/', include('line_bot.urls')),
	url(r'^runbatchop/', RunBatchOP), 
	url(r'^line_login/', line_login), 
	url(r'^GetLineNotify/', GetLineNotify), 
	url(r'^gettokenfromcode/', GetTokenFromCode), 
	url(r'^subscribe_bot/', subscribe_bot), 
    url(r'^writeDB_bot/', writeDB_bot),
    url(r'^writeDB_bot2/', writeDB_bot2),
    url(r'^stoptoday/', stoptoday),
    url(r'^RunBatchnonstop/', RunBatchnonstop),
    url(r'^RunBatchGetRate/', RunBatchGetRate),
    

]
