"""
ASGI config for matataBlog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path,path
from channels.security.websocket import AllowedHostsOriginValidator
from blog.consumers import BlogConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matataBlog.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/allPosts/',BlogConsumer.as_asgi()),                
            ])
        )
    ),
})


