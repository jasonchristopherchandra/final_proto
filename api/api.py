import flask
from flask import Flask, request, jsonify
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def translate(str):
    str = "sudah di edit"
    return str

@app.route('/', methods=['GET'])
def home():
    return "<h1>Proto Translation API for chat translator.</p>"

# GET requests will be blocked
@app.route('/translate_view', methods=['POST'])
def translate_view():
    request_data = request.get_json()
    print(request_data)
    print(request.data)

    author = None
    message = None
    trans_auth = None
    trans_mess = None

    if request_data:
        if 'author' in request_data:
            author = request_data['author']
            trans_auth = translate(author)

        if 'message' in request_data:
            message = request_data['message']
            trans_mess = translate(message)

    return trans_auth, trans_mess

@app.route('/translate_send', methods=['POST'])
def translate_send():
    request_data = request.get_json()

    author = None
    message = None

    if request_data:
        if 'author' in request_data:
            author = request_data['author']

        if 'message' in request_data:
            message = request_data['message']

    return '''
           The author value is: {}
           The message value is: {}
           The boolean value is: {}'''.format(author,  message)


app.run()