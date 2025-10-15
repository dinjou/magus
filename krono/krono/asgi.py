"""
ASGI config for krono project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krono.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Import routing after Django is set up
# from magus import routing as magus_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # WebSocket routing will be added when we implement real-time features
    # "websocket": AllowedHostsOriginValidator(
    #     URLRouter(
    #         magus_routing.websocket_urlpatterns
    #     )
    # ),
})
