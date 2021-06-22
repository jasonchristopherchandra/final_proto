from django.http import HttpResponseRedirect
from django.shortcuts import render
from .functions import send_message,view_message,check_active_livechat

from django.core.exceptions import PermissionDenied
from django.contrib import messages
import pytchat 

def enter_url(request):
    if request.user.is_authenticated:
        return render(request, "enter_url.html")
    else:
        raise PermissionDenied()

def retrieveURL(request):
    if request.user.is_authenticated:
        title = ""
        context = {}
        if request.method == "POST":
            title = str(request.POST.get('URL'))
            if title == '':
                messages.warning(request, 'Please enter url !')
                return render(request, 'enter_url.html')
            print(title)
            print(isinstance(title, str))
            livechatstatus = check_active_livechat(title,request)
            videoDetails = {'title':title}
            context = {'title':title,'livechatstatus':livechatstatus}
            return render(request, "viewsend.html",  context)
    else:
        raise PermissionDenied()
    
