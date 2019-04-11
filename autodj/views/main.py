import json
import requests
from random import randint
from flask import (
    Blueprint, Response, render_template, request, session
)

from autodj.views.auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

@bp.route('/song', methods=(["POST"]))
def song():
    access_token = session.get('access_token')

    songs = json.loads(request.form['songs'])
    # topic = request.form['topic']

    tracks_to_add = []

    search_url = "https://api.spotify.com/v1/search"
    item_type = "track"
    headers = {
        "Authorization": "Bearer " + access_token
    }

    song = songs[randint(0, len(songs)-1)]
    search_query = "track:" + song['song'] + " artist:" + song['artist']
    params = {
        "q": search_query,
        "type": item_type,
    }
    song_response = requests.get(search_url, params=params, headers=headers)
    song_response = song_response.json()
    if len(song_response['tracks']['items']) > 0:
        uri = song_response['tracks']['items'][0]['uri'] # get uri of first result
        tracks_to_add.append(uri)

    # for song in songs:
    #     search_query = "track:" + song['song'] + " artist:" + song['artist']
    #     params = {
    #         "q": search_query,
    #         "type": item_type,
    #     }
    #     song_response = requests.get(search_url, params=params, headers=headers)
    #     song_response = song_response.json()
    #     if len(song_response['tracks']['items']) > 0:
    #         uri = song_response['tracks']['items'][0]['uri'] # get uri of first result
    #         tracks_to_add.append(uri)

    play_url = "https://api.spotify.com/v1/me/player/play"
    body = {
        "uris": tracks_to_add
    }
    play_response = requests.put(url=play_url, json=body, headers=headers)
    return Response(
        status=200,
        response=json.dumps({"play_response": "" + song['song'] + " by " + song['artist']})
        )
    

@bp.route('/playlist', methods=(["POST"]))
def playlist():
    access_token = session.get('access_token')

    songs = json.loads(request.form['songs'])
    topic = request.form['topic']

    # create playlist with name of topic
    user_id = session.get('user_id')
    playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data = {
        "name": "AutoDJ " + topic
    }
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    playlist_response = requests.post(playlist_url, data=json.dumps(data), headers=headers).json()
    playlist_id = playlist_response['id']

    tracks_to_add = []

    search_url = "https://api.spotify.com/v1/search"
    item_type = "track"
    headers = {
        "Authorization": "Bearer " + access_token
    }

    for song in songs:
        search_query = "track:" + song['song'] + " artist:" + song['artist']
        params = {
            "q": search_query,
            "type": item_type,
        }
        song_response = requests.get(search_url, params=params, headers=headers)
        song_response = song_response.json()
        if len(song_response['tracks']['items']) > 0:
            uri = song_response['tracks']['items'][0]['uri'] # get uri of first result
            tracks_to_add.append(uri)

    add_to_playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    data = {
        "uris": tracks_to_add
    }

    add_to_playlist_response = requests.post(add_to_playlist_url, data=json.dumps(data), headers=headers)
    embed_playlist_link = F"https://open.spotify.com/embed/user/{user_id}/playlist/{playlist_id}"
    if add_to_playlist_response.status_code == 201:
        response = {
            "status": 200,
            'message': "success",
            "embed_link": embed_playlist_link
        }
    else:
        # something went wrong
        response = {
            "status": 400,
            "message": "something went wrong",
            "embed_link": embed_playlist_link
        }

    return Response(
        status=response['status'],
        response=json.dumps(response)
    )
