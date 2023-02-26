"""
ASGI config for file_storage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from api import consumers,routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_storage.settings')





# ws_pattern = [
#     path('ws/test/',consumers.MyConsumer)
# ]

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": URLRouter(routing.websockets_urlpatterns)
})