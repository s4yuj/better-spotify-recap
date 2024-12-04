import spotipy
import os
import streamlit
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

#TODO: look into most effective scope for application
SCOPE = "user-top-read"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000"

print(CLIENT_ID)
print(CLIENT_SECRET)


sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = CLIENT_ID, 
    client_secret = CLIENT_SECRET, 
    redirect_uri = REDIRECT_URI,
    scope=SCOPE))

# streamlit.set_page_config(page_title="Better spotify recap", page_ico=":eggplant:")
# streamlit.title("Better Spotify Recap")
# streamlit.write("This is a better spotify recap")

top_tracks = sp.current_user_top_tracks(limit=10, time_range="long_term")

print(top_tracks)