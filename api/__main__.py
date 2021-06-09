from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
import re
import math
from io import open
import numpy as np
import matplotlib.pyplot as plt
import pickle

# import torch
# from torch.autograd import Variable
# import torch.nn as nn
# import torch.nn.functional as F
# from torch import optim
# import torch.cuda

# this line clears sys to allow for argparse to work as gradient clipper
import sys; sys.argv=['']; del sys

app = Flask(__name__)
CORS(app, support_credentials=True)
# bidirectional = True
# if bidirectional:
# 	directions = 2
# else:
# 	directions = 1

# # number of layers in both the Encoder and Decoder
# layers = 4

# # Hidden size of the Encoder and Decoder
# hidden_size = 800

# # Dropout value for Encoder and Decoder
# dropout = 0.5

# # LOAD CONFIGURATIONS

# # Set the common name of the loading files
# common_file_name = "testdata.tatoeba_identic_trim.20_vocab.25000_directions.2_layers.4_hidden.100_dropout.0.5_learningrate.1_batch.10_epochs.100"
# id_lang = 'id'
# en_lang = 'en'
# dataset = 'tatoeba_identic'
# directory = ''

# # Set the name of the loading files
# id_vocab_file = directory + id_lang + '_14947_' + dataset + '_vocab.p'
# en_vocab_file = directory + en_lang + '_15096_' + dataset + '_vocab.p'
# id_en_enc_file = '%s_%s_enc_direction_%s_layer_%s_hidden_%s_dropout_%s.pth' % (id_lang, en_lang, directions, layers, hidden_size, dropout)
# id_en_dec_file = '%s_%s_dec_direction_%s_layer_%s_hidden_%s_dropout_%s.pth' % (id_lang, en_lang, directions, layers, hidden_size, dropout)
# en_id_enc_file = '%s_%s_enc_direction_%s_layer_%s_hidden_%s_dropout_%s.pth' % (en_lang, id_lang, directions, layers, hidden_size, dropout)
# en_id_dec_file = '%s_%s_dec_direction_%s_layer_%s_hidden_%s_dropout_%s.pth' % (en_lang, id_lang, directions, layers, hidden_size, dropout)

# # Mandatory variables initialization
# device = torch.device('cpu')
# use_cuda = torch.cuda.is_available()
# id_vocab = None
# en_vocab = None
# id_en_encoder = None
# id_en_decoder = None
# en_id_encoder = None
# en_id_decoder = None

# # LOAD EVERYTHING

# id_vocab = pickle.load(open(id_vocab_file,'rb'))
# en_vocab = pickle.load(open(en_vocab_file,'rb'))

# id_en_encoder = EncoderRNN(id_vocab.vocab_size, hidden_size, layers=layers, 
#                            dropout=dropout, bidirectional=bidirectional)
# id_en_decoder = DecoderAttn(hidden_size, en_vocab.vocab_size, layers=layers, 
#                             dropout=dropout, bidirectional=bidirectional)

# id_en_encoder.load_state_dict(torch.load(id_en_enc_file, map_location=device))
# id_en_decoder.load_state_dict(torch.load(id_en_dec_file, map_location=device))

# id_en_encoder.eval()
# id_en_decoder.eval()
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
    # print(request_data, file=sys.stderr)
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
    print(request_data)
    message = None

    if request_data:
        if 'message' in request_data:
            message = "message changed from " + request_data['message'] + " to translated"

    return jsonify({'message':message})


app.run(host='0.0.0.0', port=5000, debug=True)