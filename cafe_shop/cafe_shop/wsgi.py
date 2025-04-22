"""
WSGI config for cafe_shop project.

It exposes the WSGI callable as a module-level variable named ``application``. 
This file is used for synchronous deployment with WSGI servers like Gunicorn.

For more information, see: https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_shop.settings')
application = get_wsgi_application()