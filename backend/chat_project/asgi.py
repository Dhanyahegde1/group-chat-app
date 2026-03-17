import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_project.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat_project.routing


application = ProtocolTypeRouter({

    "http": get_asgi_application(),

    "websocket": URLRouter(
        chat_project.routing.websocket_urlpatterns
    ),

})

