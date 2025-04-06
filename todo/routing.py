# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from todo.consumers import TimerConsumer

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path("ws/timer/<int:task_id>/", consumers.TimerConsumer.as_asgi()),
#         ])
#     ),
# })

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/timer/(?P<task_id>\d+)/$", consumers.TimerConsumer.as_asgi()),
]

