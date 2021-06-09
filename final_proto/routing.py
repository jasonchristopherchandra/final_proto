from django.urls import re_path

import tester4

websocket_urlpatterns = [
    re_path(r'start_chat/', tester4.ChatConsumer.as_asgi()),
]