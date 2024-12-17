import spotipy
import json
import datetime
from flask import session
import time

def get_access_token():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("Token not found")
    # return token_info['access_token']

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        print("token expired!!!!!!")

    return token_info['access_token']


def get_stat() -> dict:
    token = get_access_token()
    sp = spotipy.Spotify(auth=token)

    res = {}

    total = 1
    offset = 0

    while offset < total:
        response = sp.current_user_top_tracks(limit=50, time_range="short_term", offset=offset)

        total = response['total']
        for idx, track in enumerate(response['items']):
            res[offset+idx] = {
                'ID' : track['id'],
                'Name' : track['name'],
                'Album' : track['album']['name'],
                'Artist' : track['artists'][0]['name'], #TODO: handle multiple artists
                'Release Date' : track['album']['release_date'],
                'Popularity' : track['popularity'],
                'Explicit' : track['explicit'],
                'Duration' : track['duration_ms'],
                }
        offset += 50

    with open('output_top_tracks.json', "w") as f:
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} top tracks to output file")

    # audio_features = get_music_data(res)

    return res

def get_recently_played() -> dict:
    token = get_access_token()
    sp = spotipy.Spotify(auth=token)

    res = {}

    response = sp.current_user_recently_played(limit=50, after=int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000))

    for idx, item in enumerate(response['items']):
        track = item['track']
        res[idx] = {
            'ID' : track['id'],      
            'Name' : track['name'],
            'Album' : track['album']['name'],
            'Artist' : track['artists'][0]['name'],
            'Release Date' : track['album']['release_date'],            
            'Popularity' : track['popularity'],
            'Explicit' : track['explicit'],
            'Duration' : track['duration_ms'],
            'Played At' : item['played_at']
            }

    with open("output_recently_played.json", "w") as f:
        #dump final result into output file
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} recently played to output file")

    # audio_features = get_music_data(res)

    # with open('raw_recently_played.json', "w") as f:
    #     #dump raw data into output file
    #     json.dump(response['items'], f, indent=4)
    return res

# def get_music_data(data :dict) -> list:
#     token = get_access_token()
#     sp = spotipy.Spotify(auth=token)
    
#     print("audio features Token: ", token)

#     track_ids = [data[key]['ID'] for key in data]
#     print(track_ids)

#     # audio_features = sp.audio_features(tracks = track_ids)

#     headers = {
#         'Authorization': f'Bearer {token}'
#     }
#     url = f"https://api.spotify.com/v1/audio-features/?ids={','.join(track_ids)}"
#     response = requests.get(url, headers=headers)
    
#     print("Response Headers:", response.headers)
#     response.raise_for_status()  # This will raise an HTTPError if the response was an HTTP error

#     audio_features = response.json()


#     with open("output_audio_features.json", "w") as f:
#         json.dump(audio_features, f, indent=4)

#     return audio_features
