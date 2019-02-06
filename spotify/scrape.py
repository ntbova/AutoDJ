import os
import spotipy
import json
import sys
import spotipy.util as util

username = sys.argv[1]

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)
    # print('wat?')

spotify = spotipy.Spotify(auth=token)


if len(sys.argv) > 2:
    name = ' '.join(sys.argv[2:])
else:
    name = 'Radiohead'

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])
