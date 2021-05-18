from urllib.parse import urlparse, parse_qs
from pprint import pprint
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from pytchat import LiveChat, CompatibleProcessor
from chat_downloader import ChatDownloader
import time
import pytchat
import subprocess
import shlex

def extract_video_id(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    print(query)
    # fail?
    return None


def send_message(url, message,request):
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

    print(response)
    #gets active livechat id and channelid
    channelid = response['items'][0]['snippet']['channelId']
    # print("this is the channel id: " + response['items'][0]['snippet']['channelId'])
    # print("you are currently watching " + response['items'][0]['snippet']['title'] + " by: " + response['items'][0]['snippet']['channelTitle'])
    if response['items'][0]['snippet']['liveBroadcastContent'] == 'none':
        print("hey this isnt a live stream, checking if this is an archive")
        chat = ChatDownloader().get_chat(url)       # create a generator
        for message in chat:
            print(chat.format(message))     
        return render(request, 'index.html')
    else:
        livechatid = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    # print("this is the livechat id: " + response['items'][0]['liveStreamingDetails']['activeLiveChatId'])
    #prints out all live chat messages
    # response1 = service.liveChatMessages().list(
    #         liveChatId = livechatid,
    #         part = 'snippet'
    #     ).execute()

    print(response1)
    #sends out a message to the live chat 
    # response2 = service.liveChatMessages().insert(
    #     part = 'snippet',
    #     body = dict (
    #         snippet = dict(
    #             liveChatId = livechatid,
    #             type = "textMessageEvent",
    #             textMessageDetails = dict(
    #                 messageText = message
    #             )
    #         )
    #     )  
    # ).execute()

    # print(response2)

def view_message(url,request):
    id = extract_video_id(url)
    print(id)
    proc = subprocess.Popen(shlex.split('python3 tester3.py ' + str(url)))
    stdout = proc.communicate()[0]
    print("is this weird")

    # token = SocialToken.objects.get(account__user=request.user, account__provider='google')
    # print(token)
    # # CLIENT_SECRET_FILE = 'client_secret_51870834106-rtq1bi2n4n6cme450auv0iffv9fpokre.apps.googleusercontent.com.json'
    # # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    # credentials = Credentials(
    #     token=token.token,
    #     refresh_token=token.token_secret,
    #     token_uri='https://oauth2.googleapis.com/token',
    #     client_id='375686044917-4ip2r585igrkf6kesp3ggmfd45f53433.apps.googleusercontent.com', # replace with yours 
    #     client_secret='HZgBiq-fG0_vrfsxHHNA7Ptu') # replace with yours 
    # print("secret token:"+ " "+credentials.refresh_token)
    # service = build('youtube', 'v3', credentials=credentials)
    # print(service)
    

    # part_string = 'snippet,liveStreamingDetails'
    # video_ids = id
    # #find data using API regarding video
    # print(id)
    # response = service.videos().list(
    #     part=part_string,
    #     id=video_ids
    # ).execute()

    # print(response)
    # #gets active livechat id and channelid
    # channelid = response['items'][0]['snippet']['channelId']
    # # print("this is the channel id: " + response['items'][0]['snippet']['channelId'])
    # # print("you are currently watching " + response['items'][0]['snippet']['title'] + " by: " + response['items'][0]['snippet']['channelTitle'])
    # if response['items'][0]['snippet']['liveBroadcastContent'] == 'none':
    #     print("hey this isnt a live stream, checking if this is an archive")
    #     chat = ChatDownloader().get_chat(url)       # create a generator
    #     for message in chat:
    #         print(chat.format(message))    
    #         context = {'message':chat.format(message)} 
    # else:
    #     livechatid = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    # print("this is the livechat id: " + response['items'][0]['liveStreamingDetails']['activeLiveChatId'])
    # response1 = service.liveChatMessages().list(
    #         liveChatId = livechatid,
    #         part = 'snippet'
    #     ).execute()
    # print(type(response1))
    # print(type(response1['items']))
    
    # context1 = {} 
    # for i in range(len(response1['items'])):
    #     message = response1['items'][i]['snippet']['textMessageDetails']['messageText']
    #     response2 = service.channels().list(
    #         id = response1['items'][i]['snippet']['authorChannelId'],
    #         part = 'snippet'
    #     ).execute()
    #     author = response2['items'][0]['snippet']['title']
    #     context1['message_entry '+ str(i)] = { "author" : author, 'message':message}
    # chat = ChatDownloader().get_chat(url)       # create a generator
    # for message in chat:
    #     print(chat.format(message))    
    #     context1 = {'message':chat.format(message)} 
    #  
    #sends out a message to the live chat 
    # response2 = service.liveChatMessages().insert(
    #     part = 'snippet',
    #     body = dict (
    #         snippet = dict(
    #             liveChatId = livechatid,
    #             type = "textMessageEvent",
    #             textMessageDetails = dict(
    #                 messageText = message
    #             )
    #         )
    #     )  
    # ).execute()

    # print(response2)

