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
import asyncio
from channels.consumer import AsyncConsumer
import subprocess
import shlex

print('reached')
URL = None
token = None

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event,URL=None,token=None):
        print("connected", event)
        print
        print(URL)
        print(token)
        await self.send({
            "type": "websocket.accept"
        })
        print(str(sys.argv[0]))

    


    async def websocket_receive(self, event):
        print("receive", event)
        is_connected=True
        data = json.loads(event['text'])
        print(data)
        url = data['url']
        print(url)
        token = data['token']
        print(token)
        global substart 
        substart = subprocess.Popen(shlex.split('python3 tester3.py ' + str(url) +" "+ str(token)))

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        substart.terminate()

