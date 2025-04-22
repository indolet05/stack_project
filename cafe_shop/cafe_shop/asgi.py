"""
ASGI config for cafe_shop project.

It exposes the ASGI callable as a module-level variable named ``application``. 
This file is used for asynchronous deployment with ASGI servers like Daphne or Uvicorn.

For more information, see: https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_shop.settings')
application = get_asgi_application()