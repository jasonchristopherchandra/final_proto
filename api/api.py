from flask import Flask, request, jsonify

import sys

app = Flask(__name__)
# app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Proto Translation API for chat translator.</p>"

# GET requests will be blocked
@app.route('/translate_view', methods=['POST'])
def translate_view():
    request_data = request.get_json()
    print(request_data, file=sys.stderr)
    author = None
    message = None
    translated_message = None

    if request_data:
        if 'author' in request_data:
            author  = request_data['author']

        if 'message' in request_data:
             message  = request_data['message']
             translated_message = "OK message accepted"
        

    return jsonify({'author':author,'message':message,'translated_message':translated_message})

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