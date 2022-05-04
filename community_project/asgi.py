import os
import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_project.settings')
django.setup()

import chat.routing

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
      URLRouter(
          chat.routing.websocket_urlpatterns
      )
  ),
  # Just HTTP for now. (We can add other protocols later.)
})