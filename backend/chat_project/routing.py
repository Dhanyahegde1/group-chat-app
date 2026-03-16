from django.urls import re_path
from messaging.consumers import ChatConsumer, DMConsumer

#defining websocket endpoint
websocket_urlpatterns = [
    # Group channel chat  —  now requires username in URL
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<username>\w+)/$', ChatConsumer.as_asgi()),

    # Direct messages
    re_path(r'ws/dm/(?P<my_username>\w+)/(?P<other_username>\w+)/$', DMConsumer.as_asgi()),
]