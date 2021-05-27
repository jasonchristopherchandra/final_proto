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

cur_path = os.path.dirname(__file__)
print(cur_path)

new_path = os.path.join(cur_path, 'static', "chatlist.txt")

cred = credentials.Certificate("chattranslator-2c03a-firebase-adminsdk-8554s-175f86d014.json")
firebase_admin.initialize_app(cred)

print(str(sys.argv[1]))
chat = ChatDownloader().get_chat(str(sys.argv[1])) 

# for message in chat:
#     return chat.format(message)
# print(chat)      # create a generator
print(type(chat))

def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text)


for message in chat:
    chatlist  = { }                      # iterate over messages
    chatlist['author'] = message['author']['name'].encode("ascii", errors="ignore").decode()
    chatlist['message'] = message['message'].encode("ascii", errors="ignore").decode()
    url = 'http://127.0.0.1:5000/translate_view'
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
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    time.sleep(0.1)
    # with open('chatlist'+str(sys.argv[1])+'.txt', 'a+') as file:
    #   file.write(json.dumps(response.json()))
    #   file.write('\n')

