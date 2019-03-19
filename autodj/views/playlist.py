import functools
import requests
import json

from flask import (
    Response, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('playlist', __name__, url_prefix='/playlist')


@bp.route('/', methods=(["POST"]))
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
	playlist_response =  requests.post(playlist_url, data=json.dumps(data), headers=headers).json()
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
			"message": "something when wrong",
			"embed_link": embed_playlist_link
		}

	return Response(
					status=response['status'],
					response=json.dumps(response)
					)
