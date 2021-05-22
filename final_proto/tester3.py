from chat_downloader import ChatDownloader
import sys
import json
import re
import emoji
import requests 

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
    with open('chatlist.txt', 'a+') as file:
      file.write(json.dumps(response.json()))
    #   call the translation api before dumpong into the original file 
