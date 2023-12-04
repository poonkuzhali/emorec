import os
from pathlib import Path

import openai
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from keras.models import load_model

from integrations.spotify_integration import login_spotify, callback, get_tracks
from integrations.tmdb_integration import discover_movies
from sentiment_model.prediction import get_emotions
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
loaded_model = load_model('./sentiment_model/Emotion_Recognition.h5')
openai.api_key = os.environ.get("OPENAI_KEY")
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
    try:
        message = request.args.get('userMessage')
        if message.lower() == 'bye':
            return get_emotions(loaded_model, userMessages)
        userMessages.append(message)
        messages.append({"role": "user", "content": message if message else ""})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        return reply
    except Exception as ex:
        print(ex)

@app.route('/spotify', methods=['GET'])
@cross_origin()
def get_login_spotify():
    auth_url = login_spotify()
    return auth_url

@app.route('/callback')
@cross_origin()
def spotify_callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    token_info = ''
    if 'code' in request.args:
        token_info = callback(request.args['code'])

    return token_info

@app.route('/playlist')
@cross_origin()
def spotify_playlist():
    try:
        token = request.args.get('token')
        emotion = request.args.get('emotion')
        playlist_url = get_tracks(token, emotion)
        return playlist_url
    except Exception as ex:
        print(ex)

@app.route('/movies')
@cross_origin()
def get_movies():
    try:
        emotion = request.args.get('emotion')
        result = discover_movies(emotion)
        return result
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    app.run(debug=True)