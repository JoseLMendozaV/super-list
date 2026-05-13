"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing

# Apunta a la configuración de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Configuración del enrutador ASGI
application = ProtocolTypeRouter({
    # Maneja las peticiones tradicionales (vistas, carga de página inicial)
    "http": get_asgi_application(),
    
    # Maneja las conexiones en tiempo real (cuando el navegador abre el WebSocket)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})