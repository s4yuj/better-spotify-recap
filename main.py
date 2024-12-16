import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for
from spotipy.cache_handler import FlaskSessionCacheHandler
import json

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
    
    top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")
    #pretty print the json object
    with open('output_tracks.json', "w") as f:
        json.dump(top_tracks, f, indent=4)
        print(f'length of recently played json: {len(top_tracks["items"])}')

    top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')
    with open('output_artists.json', "w") as f:
        json.dump(top_artists, f, indent=4)
        print(f'length of recently played json: {len(top_artists["items"])}')

    current_time=int(time.time()*1000)
    one_month_ago = current_time - (28 * 24 * 60 * 60 * 1000)  # 7 days in milliseconds

    recently_played = sp.current_user_recently_played(limit=50, after=one_month_ago)
    with open("output_recently_played.json", "w") as f:
        json.dump(recently_played, f, indent=4)
        print(f'length of recently played json: {len(recently_played["items"])}')

    return "Check the output files"
if __name__ == '__main__':
    app.run(debug = True)