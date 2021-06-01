from django.urls import path

from . import views
from django.views.generic import TemplateView
from .functions import send_message,display_text,view_message,close_subprocess
urlpatterns = [
   path('input_test/', views.get_name, name = "test_input"),
   path('yt_caller/', send_message, name = "call_yt"),
   path('get_url/', views.retrieveURL, name = "url_getter"),
   path('display_text/', display_text, name = "get_translated_messages"),
   path('view_message/', view_message, name = "get_translated_messages"),
   path('close_subprocess/', close_subprocess, name = "close_subprocess"),
   
   # path('firebase-messaging-sw.js', views.ServiceWorkerView.as_view(), name='service_worker')
]
