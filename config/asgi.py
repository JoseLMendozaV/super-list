"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# 1. Apunta a los settings de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. INICIALIZA DJANGO PRIMERO (Esta es la línea que soluciona el error)
django_asgi_app = get_asgi_application()

# 3. AHORA SÍ importamos Channels y tus rutas, porque Django ya está listo
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns

# 4. Enrutador principal
application = ProtocolTypeRouter({
    # Maneja el tráfico HTTP normal
    "http": django_asgi_app,
    
    # Maneja los WebSockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})