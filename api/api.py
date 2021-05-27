from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys

app = Flask(__name__)
CORS(app, support_credentials=True)
# app.config["DEBUG"] = True

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
@cross_origin(supports_credentials=True)
def translate_send():
    request_data = request.get_json()

    message = None

    if request_data:
        if 'message' in request_data:
            message = "message changed from " + request_data['message'] + " to translated"

    return jsonify({'message':message})


app.run(host='0.0.0.0', port=5000, debug=True)