from urllib.parse import urlparse, parse_qs

from pprint import pprint
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp

import pytchat 
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
    # fail?
    return None

#takes id input to find specific video from url
id = extract_video_id("https://www.youtube.com/watch?v=5qap5aO4i9A")

# CLIENT_SECRET_FILE = 'client_secret_51870834106-rtq1bi2n4n6cme450auv0iffv9fpokre.apps.googleusercontent.com.json'
# API_NAME = 'youtube'
# API_VERSION = 'v3'
# SCOPES = ['https://www.googleapis.com/auth/youtube']

token = SocialToken.objects.get(account__user=request.user, account__provider='google')

credentials = Credentials(
    token=token.token,
    refresh_token=token.token_secret,
    token_uri='https://oauth2.googleapis.com/token',
    client_id='375686044917-4ip2r585igrkf6kesp3ggmfd45f53433.apps.googleusercontent.com', # replace with yours 
    client_secret='HZgBiq-fG0_vrfsxHHNA7Ptu') # replace with yours 

service = build('youtube', 'v3', credentials=credentials)

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
print("this is the channel id: " + response['items'][0]['snippet']['channelId'])
print("you are currently watching " + response['items'][0]['snippet']['title'] + " by: " + response['items'][0]['snippet']['channelTitle'])
livechatid = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
print("this is the livechat id: " + response['items'][0]['liveStreamingDetails']['activeLiveChatId'])
#prints out all live chat messages
response1 = service.liveChatMessages().list(
        liveChatId = livechatid,
        part = 'snippet'
    ).execute()

print(response1)
#sends out a message to the live chat 
response2 = service.liveChatMessages().insert(
    part = 'snippet',
    body = dict (
        snippet = dict(
            liveChatId = livechatid,
            type = "textMessageEvent",
            textMessageDetails = dict(
                messageText = "demo insert"
            )
        )
    )  
).execute()

print(response2)


