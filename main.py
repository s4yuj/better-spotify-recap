import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for
from spotipy.cache_handler import FlaskSessionCacheHandler
import json
import utils

load_dotenv()

app = Flask(__name__)
#a session is like a container that can store data -- this data is available across requests
#we will store the spotify access tokens in the session data

#we dont want users tampering with that data. So we use a secret key to encrpyt the data
app.config['SECRET_KEY'] = os.urandom(69)

cache_handler = FlaskSessionCacheHandler(session)

#TODO: look into most effective scope for application
SCOPE = "user-top-read user-read-recently-played"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

sp_oauth = SpotifyOAuth(
    client_id = CLIENT_ID, 
    client_secret = CLIENT_SECRET, 
    redirect_uri = REDIRECT_URI,
    scope=SCOPE,
    cache_handler=cache_handler,
    show_dialog=True)
sp = spotipy.Spotify(auth_manager = sp_oauth)

#this is the home endpoint
@app.route('/')
def home():
    #check if token is valid and present
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        #get_authorize_url() returns the URL to authorize spotify
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('results'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('results'))

@app.route('/results')
#this might be the place where you should abstract out the model logic to another file
def results():
    if not sp_oauth.get_authorize_url(cache_handler.get_cached_token()):
        auth_url = sp.oauth.get_authorize_url()
        return redirect(auth_url)
    
    top_tracks = utils.get_stat(sp)

    recently_played = utils.get_recently_played(sp)

    for track in recently_played.values():
        # print(track["Name"])
        pass

    return "Check the output files"

if __name__ == '__main__':
    app.run(debug = True)