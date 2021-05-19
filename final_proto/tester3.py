from chat_downloader import ChatDownloader
import sys
import json
import re
import emoji

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
     with open('chatlist.txt', 'a+') as file:
      file.write(json.dumps(chatlist, indent=2))