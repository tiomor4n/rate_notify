from .base import *

SECRET_KEY = 'hhnpfo*jc@a!%lgm7-q#4h9noj9v1kwm(d*=l2eji1#878vmd@'
DEBUG = False
TEMPLATE_DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}