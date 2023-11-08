import base64
import hashlib

import requests
import urllib.parse

import secrets
import string


CLIENT_ID = 'c1d761fe921947378815d5270ed7c314'
CLIENT_SECRET = '6fd9b1941d3f4c5eb85018dfdf31480d'

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1'
TOP_ARTISTS = '/me/top/artists'
FOLLOWING = '/me/following'


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
    hashed = sha256(code_verifier)
    code_challenge = base64urlencode(hashed)

    scope = 'user-read-private user-read-email user-top-read user-follow-read'

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

client_creds = f'{CLIENT_ID}:{CLIENT_SECRET}'
b64_client_creds = base64.b64encode(client_creds.encode())

def callback(code):
    req_body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        # 'client_secret': CLIENT_SECRET,
        'code_verifier': code_verifier
    }

    response = requests.post(TOKEN_URL, data=req_body, headers= {'Content-Type': 'application/x-www-form-urlencoded',
                                                                 'Authorization': f'Basic {b64_client_creds.decode()}',})
    token_info = response.json()
    print(token_info['access_token'])
    top_artists_name, top_artists_id =get_users_favorite_artists(token_info['access_token'])
    get_recommendations(top_artists_id, token_info['access_token'])
    return token_info


def get_users_favorite_artists(token):
    top_artists_name = []
    top_artists_id = []
    response = requests.get(f'{BASE_URL}{TOP_ARTISTS}', headers={'Authorization': f'Bearer {token}'})
    response_json = response.json()

    for item in response_json['items']:
        if item['name'] not in top_artists_name:
            top_artists_name.append(item['name'])
            top_artists_id.append(item['id'])

    response = requests.get(f'{BASE_URL}{FOLLOWING}?type=artist', headers={'Authorization': f'Bearer {token}'})
    response_json = response.json()

    print('top artists')
    for item in response_json['artists']['items']:
        if item['name'] not in top_artists_name:
            top_artists_name.append(item['name'])
            top_artists_id.append(item['id'])

    return top_artists_name, top_artists_id

def get_artists_top_tracks(top_artists, token):
    top_tracks_id = []
    for artist in top_artists:
        response = requests.get(f'{BASE_URL}/artists/{artist}/top-tracks', headers={'Authorization': f'Bearer {token}'})
        response_info = response.json()
        tracks_info = response_info['tracks']
        for track in tracks_info:
            top_tracks_id.append(track['id'])

    return top_tracks_id

def get_recommendations(top_artists, token):
    print('reco')
    seed_artists = ','.join(artist for artist in top_artists[:5])
    response = requests.get(f'{BASE_URL}/recommendations?limit=20&market=US&seed_artists={seed_artists}&max_danceability=0.9', headers={'Authorization': f'Bearer {token}'})
    json_ob = response.json()

    for track in json_ob['tracks']:
        print(track['name'])

