from chat_downloader import ChatDownloader
import sys
import json
import re
import emoji
import requests 
import os
import time
from firebase_admin import messaging,credentials
import firebase_admin


cred = credentials.Certificate("chattranslator-2c03a-firebase-adminsdk-8554s-175f86d014.json")
firebase_admin.initialize_app(cred)

print(str(sys.argv[1]))
try:
    chat = ChatDownloader().get_chat(str(sys.argv[1])) #gets yt chat message
    for message in chat:
        chatlist  = { }                      # iterate over messages
        chatlist['author'] = message['author']['name'].encode("ascii", errors="ignore").decode()
        chatlist['message'] = message['message'].encode("ascii", errors="ignore").decode()
        url = 'http://localhost:5000/translate_view' #call ai translation
        data = {
        "author": chatlist['author'],
        "message": chatlist['message'],
        }
        response = requests.post(url, json=data)
        registration_token = str(sys.argv[2])
        # See documentation on defining a message payload.
        message = messaging.Message(
            data={
                'author': response.json()['author'],
                'message': response.json()['message'],
                'translated_message': response.json()['translated_message']
            },
            token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        time.sleep(1.5)
        response = messaging.send(message)
    # Response is a message ID string.

    time.sleep(0.1)
except Exception as inst:
    print("An exception occurred")
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)    
    registration_token = str(sys.argv[2])
    message = messaging.Message(
        data={
            'author': "SYSTEM",
            'message': "VIDEO IS NOT A LIVE STREAM",
            'translated_message':"VIDEO IS NOT A LIVE STREAM"
            },
        token=registration_token,
        )
    response = messaging.send(message)