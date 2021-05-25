from django.urls import path

from . import views
from django.views.generic import TemplateView
from .functions import send_message,display_text
urlpatterns = [
   path('input_test/', views.get_name, name = "test_input"),
   path('yt_caller/', send_message, name = "call_yt"),
   path('get_url/', views.retrieveURL, name = "url_getter"),
   path('display_text/', display_text, name = "gte_translated_messages"),
   # path('firebase-messaging-sw.js', views.ServiceWorkerView.as_view(), name='service_worker')
]
