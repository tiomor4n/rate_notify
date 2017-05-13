from django.conf.urls import include, url
from django.contrib import admin
from subscribe.views import index
from subscribe.views import RunBatchOP,subscribe,logout,subsummary,GetLineNotify,GetTokenFromCode,stoptoday,getnotifyinfo,hist_data,line_login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', index),
	url(r'^line_bot/', include('line_bot.urls')),
	url(r'^runbatchop/', RunBatchOP), 
	url(r'^subscribe/', subscribe),
	url(r'^index/', index),
	url(r'^logout/', logout),
    url(r'^subsummary/', subsummary),
	url(r'^GetLineNotify/', GetLineNotify),
    url(r'^gettokenfromcode/', GetTokenFromCode),
    url(r'^stoptoday/', stoptoday),
	 url(r'^getnotifyinfo/', getnotifyinfo),  
	 url(r'^hist_data/', hist_data), 
    url(r'^line_login/', line_login), 
]
