import dj_database_url
from django.conf import settings
 
# Set delpoy
DEBUG = False
TEMPLATE_DEBUG = False
 
# Get Database object
DATABASES = settings.DATABASES
 
DATABASES['default'] = dj_database_url.config()
 
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
 
# Allow all host headers
ALLOWED_HOSTS = ['*']