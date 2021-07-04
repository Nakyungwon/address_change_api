# import address.routing
# import address.routing
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import re_path
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # path('sockettest', consumers.ChatConsumer)
]

# rootapp/routing.py
# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             # address.routing.websocket_urlpatterns
#             websocket_urlpatterns
#         )
#     ),
# })
