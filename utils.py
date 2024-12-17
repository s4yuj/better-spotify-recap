import spotipy
import json
import datetime

def get_stat(instance: spotipy.client.Spotify) -> list:
    res = {}

    total = 1
    offset = 0

    while offset < total:
        response = instance.current_user_top_tracks(limit=50, time_range="short_term", offset=offset)

        total = response['total']
        for idx, track in enumerate(response['items']):
            res[offset+idx] = {      
                'Track' : track['name'],
                'Album' : track['album']['name'],
                'Artist' : track['artists'][0]['name'],
                'Release Date' : track['album']['release_date'],            
                'Track Number' : track['track_number'],
                'Popularity' : track['popularity'],
                'Explicit' : track['explicit'],
                'Duration' : track['duration_ms'],
                'Audio Preview URL' : track['preview_url'],
                'Album URL' : track['album']['external_urls']['spotify']
                }
        offset += 50

                
    with open('output_tracks.json', "w") as f:
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} top tracks to output file")

    return res

def get_recently_played(instance: spotipy.client.Spotify) -> list:
    res = {}

    response = instance.current_user_recently_played(limit=50, after=int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000))
    with open('output_recently_played.json', "w") as f:
        json.dump(response['items'], f, indent=4)

    for idx, item in enumerate(response['items']):
        track = item['track']
        res[idx] = {
            'Name' : track['name'],
            'Album' : track['album']['name'],
            'Artist' : track['artists'][0]['name'],
            'Release Date' : track['album']['release_date'],            
            'Track Number' : track['track_number'],
            'Popularity' : track['popularity'],
            'Explicit' : track['explicit'],
            'Duration' : track['duration_ms'],
            'Audio Preview URL' : track['preview_url'],
            'Album URL' : track['album']['external_urls']['spotify'],
            'Played At' : item['played_at']
            }

    with open("output_recently_played.json", "w") as f:
        json.dump(res, f, indent=4)
        print(f"Added {len(res)} recently played to output file")
    return res
