from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import YTForm
from .functions import send_message


import pytchat 
def get_name(request):
    # if this is a POST request we need to process the form data
    request1 = request
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YTForm(request.POST)
        # check whether it's valid:
        print(form)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message = request.POST['message']
            url = request.POST['URL']
            send_message(url, message,request1)
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YTForm()

    return render(request, 'proto.html', {'form': form})

def retrieveURL(request):
    title = ""
    if request.method == "POST":
        title = str(request.POST.get('URL'))
        print(title)
        print(isinstance(title, str))
        context = {'title':title}
        return render(request, "viewsend.html",  context)