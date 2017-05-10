from django.conf.urls import include, url
from django.contrib import admin
from subscribe.views import index
from subscribe.views import RunBatchOP

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', index),
	url(r'^line_bot/', include('line_bot.urls')),
	url(r'^runbatchop/', RunBatchOP), 
]
