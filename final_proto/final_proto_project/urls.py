"""final_proto_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from final_proto_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #...
    url(r'', include('final_proto_app.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('error/', TemplateView.as_view(template_name="500.html")),
    path('about/', TemplateView.as_view(template_name="about.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    url(r'^admin/', admin.site.urls),
     url(r'^firebase-messaging-sw.js', (TemplateView.as_view(template_name="firebase-messaging-sw.js", content_type='application/javascript', )), name='sw.js'),
    
]