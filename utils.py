import spotipy
import json
import datetime

def get_stat(instance: spotipy.client.Spotify) -> list:
    res = {}

    total = 1
    offset = 0

    while offset < total:
        response = instance.current_user_top_tracks(limit=50, time_range="short_term", offset=offset)

        # with open("raw_tracks.json", "a") as f:
        #     json.dump(response['items'], f, indent=4)
    
        total = response['total']
        for idx, track in enumerate(response['items']):
            res[offset+idx] = {      
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

    return res

def get_recently_played(instance: spotipy.client.Spotify) -> list:
    res = {}

    response = instance.current_user_recently_played(limit=50, after=int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000))

    for idx, item in enumerate(response['items']):
        track = item['track']
        res[idx] = {
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

    # with open('raw_recently_played.json', "w") as f:
    #     #dump raw data into output file
    #     json.dump(response['items'], f, indent=4)

    return res
