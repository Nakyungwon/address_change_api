from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import address.routing
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

# ASGI_APPLICATION = "app.routing.application"

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 'http': get_asgi_application,
    'websocket': AllowedHostsOriginValidator(  
        AuthMiddlewareStack(
            URLRouter(
                address.routing.websocket_urlpatterns
            )
        )
    )
})
