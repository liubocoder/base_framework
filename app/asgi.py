"""
ASGI config for base_framework project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.core.asgi import get_asgi_application

from app.api.auth.jwt import WebsocketJwtAuthMiddleware
from app.websocket.urls import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        CookieMiddleware(SessionMiddleware(WebsocketJwtAuthMiddleware(URLRouter(ws_urlpatterns))))
    )
})
