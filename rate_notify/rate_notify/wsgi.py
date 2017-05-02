"""
WSGI config for rate_notify project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rate_notify.settings")

application = get_wsgi_application()

try:
	from dj_static import Cling, MediaCling
	application = Cling(get_wsgi_application())
	application = Cling(MediaCling(get_wsgi_application()))
except:
	pass
