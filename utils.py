import spotipy
import json
import datetime
from flask import session
import time

def extract_track_info(track, additional_info=None):
    info = {
        'Name': track['name'],
        'Album': track['album']['name'],
        'Artist': track['artists'][0]['name'],  # TODO: handle multiple artists
        'Release Date': track['album']['release_date'],
        'Popularity': track['popularity'],
        'Explicit': track['explicit'],
        'Duration': track['duration_ms'],
    }
    if additional_info:
        info.update(additional_info)
    return info

def get_top_tracks() -> dict:
    token_info = session.get('token_info', None)
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)

    res = {}
    total = 1
    offset = 0
    while offset < total:
        response = sp.current_user_top_tracks(limit=50, time_range="short_term", offset=offset)

        total = response['total']
        for idx, track in enumerate(response['items']):
            res[offset+idx] = extract_track_info(track)
        offset += 50

    with open('output_top_tracks.json', "w") as f:
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} top tracks to output file")

    return res

def get_recently_played() -> dict:
    token_info = session.get('token_info', None)
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)
    
    response = sp.current_user_recently_played(limit=50, after=int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000))

    res = {}
    for idx, item in enumerate(response['items']):
        track = item['track']
        res[idx] = extract_track_info(track, {'Played At': item['played_at']})

    with open("output_recently_played.json", "w") as f:
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} recently played to output file")

    # with open('raw_recently_played.json', "w") as f:
    #     #dump raw data into output file
    #     json.dump(response['items'], f, indent=4)
    return res