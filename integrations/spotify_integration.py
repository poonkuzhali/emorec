import base64
import hashlib
import os
import random

import requests
import urllib.parse

import secrets
import string

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1'
TOP_ARTISTS = '/me/top/artists'
FOLLOWING = '/me/following'
AUDIO_FEATURES = '/audio-features'


def generate_random_string(length):
    possible_characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(possible_characters) for _ in range(length))
    return random_string

def sha256(plain):
    encoder = plain.encode('utf-8')
    return hashlib.sha256(encoder).digest()

def base64urlencode(a):
    encoded_bytes = base64.urlsafe_b64encode(a).rstrip(b'=')
    return encoded_bytes.decode('utf-8').replace('+', '-').replace('/', '_')

code_verifier = generate_random_string(64)
def login_spotify():
    try:
        hashed = sha256(code_verifier)
        code_challenge = base64urlencode(hashed)

        scope = 'user-read-private user-read-email user-top-read user-follow-read playlist-modify-public playlist-modify-private'

        params = {
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'scope': scope,
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge,
            'redirect_uri': REDIRECT_URI,
        }

        auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
        return auth_url
    except Exception as ex:
        print(ex)

client_creds = f'{CLIENT_ID}:{CLIENT_SECRET}'
b64_client_creds = base64.b64encode(client_creds.encode())

def callback(code):
    try:
        req_body = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'code_verifier': code_verifier
        }

        response = requests.post(TOKEN_URL, data=req_body, headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                                    'Authorization': f'Basic {b64_client_creds.decode()}', })
        token_info = response.json()
        token = token_info['access_token']
        return token
    except Exception as ex:
        print(ex)

def get_tracks(token, emotion):
    try:
        top_artists_name, top_artists_id = get_users_favorite_artists(token)
        top_tracks = get_artists_top_tracks(top_artists_id, token)
        recommended_tracks = get_recommendations(top_tracks, token, emotion)
        playlist_uri = create_playlist(token, recommended_tracks, emotion)
        return f'https://open.spotify.com/playlist/{playlist_uri}'
    except Exception as ex:
        print(ex)


def get_users_favorite_artists(token):
    top_artists_name = []
    top_artists_id = []
    response = requests.get(f'{BASE_URL}{TOP_ARTISTS}?limit=20', headers={'Authorization': f'Bearer {token}'})
    response_json = response.json()

    for item in response_json['items']:
        if item['name'] not in top_artists_name:
            top_artists_name.append(item['name'])
            top_artists_id.append(item['id'])

    response = requests.get(f'{BASE_URL}{FOLLOWING}?type=artist&imit=50', headers={'Authorization': f'Bearer {token}'})
    response_json = response.json()

    for item in response_json['artists']['items']:
        if item['name'] not in top_artists_name:
            top_artists_name.append(item['name'])
            top_artists_id.append(item['id'])

    return top_artists_name, top_artists_id

def get_artists_top_tracks(top_artists, token):
    top_tracks = []
    for artist in top_artists:
        response = requests.get(f'{BASE_URL}/artists/{artist}/top-tracks?market=US&limit=50', headers={'Authorization': f'Bearer {token}'})
        response_info = response.json()
        tracks_info = response_info['tracks']
        for track in tracks_info:
            top_tracks.append(track)
    print('Top tracks')
    return top_tracks

def get_tracks_audio_features(tracks, token):
    ids = ','.join(track['id'] for track in tracks)
    response = requests.get(f'{BASE_URL}{AUDIO_FEATURES}?ids={ids}',
                            headers={'Authorization': f'Bearer {token}'})
    response_info = response.json()
    return response_info['audio_features']


def create_playlist(token, track_uris, emotion):
    response = requests.get(f'{BASE_URL}/me', headers = {'Authorization': f'Bearer {token}'})
    user_id = response.json()['id']
    print('UserId')
    print(user_id)
    body = {
    "name": f"Emorec playlist - {emotion}",
    "description": "Playlist created for your current mood",
    "public": False
}
    response = requests.post(f'{BASE_URL}/users/{user_id}/playlists',
                             headers={'Authorization': f'Bearer {token}', 'Content-Type': "application/json"}, json=body)
    print(response)
    playlist_id = response.json()['id']
    playlist_uri = response.json()['uri']
    body = {
        "uris": track_uris,
        "position": 0
    }
    response = requests.post(f'{BASE_URL}/playlists/{playlist_id}/tracks',
                             headers={'Authorization': f'Bearer {token}', 'Content-Type': "application/json"},
                             json=body)
    print('tracks')
    print(response)
    return playlist_id

def get_recommendations(top_tracks, token, emotion):
    def group(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
    recommended_tracks = []
    random.shuffle(top_tracks)
    for tracks in list(group(top_tracks, 50)):
        audio_features = get_tracks_audio_features(tracks, token)
        for audio_feature in audio_features:
            if emotion == 'joy': #upbeat
                if audio_feature['valence'] > 0.8 and audio_feature['danceability'] > 0.6 and audio_feature['energy'] > 0.7:
                    recommended_tracks.append(audio_feature['uri'])
            elif emotion == 'sadness': #downbeat
                if audio_feature['valence'] < 0.5 and audio_feature['danceability'] < 0.5 and audio_feature['energy'] < 0.5:
                    recommended_tracks.append(audio_feature['uri'])
            elif emotion == 'anger': #energetic
                if audio_feature['valence'] < 0.5 and audio_feature['energy'] > 0.7:
                    recommended_tracks.append(audio_feature['uri'])
            elif emotion == 'love': #mellow
                if audio_feature['valence'] > 0.7 and audio_feature['energy'] < 0.6 and audio_feature['danceability'] > 0.4:
                    recommended_tracks.append(audio_feature['uri'])
            elif emotion == 'surprise': #mellow
                if audio_feature['loudness'] < 0.5 and audio_feature['valence'] > 0.8:
                    recommended_tracks.append(audio_feature['uri'])


    if len(recommended_tracks) > 30:
        recommended_tracks = recommended_tracks[:30]

    return recommended_tracks

