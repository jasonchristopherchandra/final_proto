import json

with open('chatlist.txt') as json_file:
    data = json.load(json_file)
    for p in data:
        print('author: ' + p['author'])
        print('message: ' + p['message'])
        print('translated message: ' + p['translated_message'])
        print('')