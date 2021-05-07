from django import forms

class YTForm(forms.Form):
    URL = forms.CharField(label='YTURL', max_length=100)
    message = forms.CharField(label='YTmessage', max_length=100)