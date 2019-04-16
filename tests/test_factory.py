import pytest
import requests
import sys
import json
from flask import url_for, session, request, Flask, jsonify, Response
from autodj import create_app

default_user = {'username': 'test', 'email': 'foxemasomu@webmail24.top', 'password': 'qwerty123'}
refresh_url = 'https://accounts.spotify.com/api/token'

default_user_refresh_token = 'AQCpOSeTeZEY5JOJzFXbvrzpqQpjRLYpmEDxcdiC-bblDhB3yhiER2Azmd2COQ-uLj6vgockdOYoTybV9kjJpEXeWhVj8P330g-b2PE8qGZJUYYMHxK7r519m1W3mcb_3qFWJw'
client_id = 'dee71a70880043d799fb3beeb6622a9d' # not secure
client_secret = 'd1f58af1e702408082984a99ec18f5f6' # not secure


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.from_pyfile('config.py', silent=True)
    app.debug = True
    app.secret_key = 'd1f58af1e702408082984a99ec18f5f6'
    return app

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['Authorization'] = 'redacted'
            auth(session)
        yield client

def auth(session):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': default_user_refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    auth_response = requests.post(refresh_url, data=data).json()


    session.clear()
    session['access_token'] = auth_response['access_token']
    session['token_type'] = auth_response['token_type']
    session['expires_in'] = auth_response['expires_in']
    session['refresh_token'] = default_user_refresh_token
    session['scope'] = auth_response['scope']

    # also get relevant user info
    user_url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization': 'Bearer ' + session.get('access_token'),
    }
    user_response = requests.get(user_url, headers=headers).json()
    session['user_id'] = user_response['id']


def test_get_root_page(client):
    # Tests for 302 code since root page currently redirects to Spotify
    index_page = client.get(url_for('index'))
    assert index_page.status_code == 302

def test_session_store(client):
    with client.session_transaction() as session:
        assert session.get('refresh_token') == default_user_refresh_token


def test_auth_session(client):
    with client.session_transaction() as session:
        assert session.get('access_token') is not None
        assert session.get('token_type') is not None
        assert session.get('scope') is not None
        assert session.get('expires_in') is not None
        assert session.get('user_id') is not None


def test_post_valid_songs_war_playlist(client):

    with open(sys.path[0] + '/valid_songs.json') as vs:
        # valid_songs = json.load(vs)
        valid_songs = vs.readlines()
        data = {
            'songs': valid_songs,
            'topic': 'War'
        }

    playlist_post = client.post(url_for('main.playlist'), data=data)
    response = playlist_post.get_json(force=True)

    assert response is not None
    assert response['status'] is 200
    assert response['embed_link'] is not None
