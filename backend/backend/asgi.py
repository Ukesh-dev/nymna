"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from core.consumer import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

ws_urlpatterns = [
    path("report/alert/", NotificationConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        ws_urlpatterns
    )
})
