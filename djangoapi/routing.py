from channels.routing import ProtocolTypeRouter, URLRouter

import alarms.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        alamrs.routing.websocket_urlpatterns
    ),
})