import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from todo.routing import websocket_urlpatterns  # Import routing file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

application = ProtocolTypeRouter({
    # HTTP requests are handled by Django (this is necessary if you also have HTTP routes)
    "http": get_asgi_application(),  # This line ensures HTTP requests are handled

    # WebSocket requests are routed to your WebSocket consumer
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # WebSocket routing
    ),
})
