from django.urls import path

from . import views
from django.views.generic import TemplateView
from .functions import send_message,view_message
urlpatterns = [
   path('send_message/', send_message, name = "call_yt"),
   path('get_url/', views.retrieveURL, name = "url_getter"),
   path('view_message/', view_message, name = "get_translated_messages"),
   path('enter_url/', views.enter_url, name='enter_url')
]
