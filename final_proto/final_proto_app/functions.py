from urllib.parse import urlparse, parse_qs
from pprint import pprint
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from pytchat import LiveChat, CompatibleProcessor
from chat_downloader import ChatDownloader
import time
import pytchat
import subprocess
import shlex
import requests
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import signal
from django.http import JsonResponse


subprocess_value = None

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    print(query)
    return None

def check_active_livechat(url, request):
    id = extract_video_id(url)
    print(id)
    token = SocialToken.objects.get(account__user=request.user, account__provider='google')
    print(token)
    # CLIENT_SECRET_FILE = 'client_secret_51870834106-rtq1bi2n4n6cme450auv0iffv9fpokre.apps.googleusercontent.com.json'
    # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='375686044917-4ip2r585igrkf6kesp3ggmfd45f53433.apps.googleusercontent.com', # replace with yours 
        client_secret='HZgBiq-fG0_vrfsxHHNA7Ptu') # replace with yours 
    print("secret token:"+ " "+credentials.refresh_token)
    service = build('youtube', 'v3', credentials=credentials)
    print(service)
    

    part_string = 'snippet,liveStreamingDetails'
    video_ids = id
    #find data using API regarding video

    response = service.videos().list(
        part=part_string,
        id=video_ids
    ).execute()
    try:
        print(response['items'][0]['liveStreamingDetails']['activeLiveChatId'])
        livechatstatus = 'alive'
        return livechatstatus
    except:
        livechatstatus = 'dead'
        return livechatstatus
    return livechatstatus

def send_message(request):
    data = json.loads(request.body.decode('UTF-8'))
    url = data['url']
    message = data['message']
    id = extract_video_id(url)
    print(id)
    token = SocialToken.objects.get(account__user=request.user, account__provider='google')
    print(token)
    # CLIENT_SECRET_FILE = 'client_secret_51870834106-rtq1bi2n4n6cme450auv0iffv9fpokre.apps.googleusercontent.com.json'
    # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='375686044917-4ip2r585igrkf6kesp3ggmfd45f53433.apps.googleusercontent.com', # replace with yours 
        client_secret='HZgBiq-fG0_vrfsxHHNA7Ptu') # replace with yours 
    print("secret token:"+ " "+credentials.refresh_token)
    service = build('youtube', 'v3', credentials=credentials)
    print(service)
    

    part_string = 'snippet,liveStreamingDetails'
    video_ids = id
    #find data using API regarding video

    response = service.videos().list(
        part=part_string,
        id=video_ids
    ).execute()

    channelid = response['items'][0]['snippet']['channelId']
    livechatid = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    response2 = service.liveChatMessages().insert(
        part = 'snippet',
        body = dict (
            snippet = dict(
                liveChatId = livechatid,
                type = "textMessageEvent",
                textMessageDetails = dict(
                    messageText = message
                )
            )
        )  
    ).execute()

    return JsonResponse("success", status=200, safe=False)

def view_message(request):
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    url = data['url']
    token = data['token']
    print(url)
    print(data)
    function_call = 'python3 tester3.py ' + str(url) +" "+ str(token)
    print("this is the function call " + function_call)
    print("is this weird")
    return HttpResponse("subprocess started")
    return JsonResponse("success",status=200, safe=False)

