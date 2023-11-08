import pickle
import re

import numpy as np
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import CORS, cross_origin
from keras.models import load_model
from keras.src.utils import pad_sequences
import openai

from integrations.spotify_integration import login_spotify, callback

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
loaded_model = load_model('./sentiment_model/Emotion_Recognition.h5')

openai.api_key = "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"

messages = [
    {"role": "system", "content": "Interact with user and ask them about their day and what they have been upto. Limit your response to 20 words"}]
userMessages = []

def main():
    while input != "bye":
        message = input()
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
@cross_origin()
def get_bot_response():
    message = request.args.get('userMessage')
    if message.lower() == 'bye':
        return get_emotions()
    userMessages.append(message)
    messages.append({"role": "user", "content": message if message else ""})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply

@app.route('/spotify', methods=['GET'])
@cross_origin()
def get_login_spotify():
    auth_url = login_spotify()
    return auth_url

@app.route('/callback')
def spotify_callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        token_info = callback(request.args['code'])

    return token_info

def get_emotions():
    with open(r"./sentiment_model/labelEncoder.pickle", "rb") as input_file:
        le = pickle.load(input_file)
    with open(r"./sentiment_model/tokenizer.pickle", "rb") as input_file:
        tokenizer = pickle.load(input_file)

    sentence = ' '.join(userMessages)
    print(sentence)
    sentence = clean(sentence)
    sentence = tokenizer.texts_to_sequences([sentence])
    sentence = pad_sequences(sentence, maxlen=256, truncating='pre')
    result = le.inverse_transform(np.argmax(loaded_model.predict(sentence), axis=-1))[0]
    proba = np.max(loaded_model.predict(sentence))
    print(f"{result} : {proba}\n\n")
    return jsonify({"emotions": result})

def clean(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()
    return text


if __name__ == '__main__':
    app.run(debug=True)