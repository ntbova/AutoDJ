import json
import functools
import requests
import base64
import urllib.parse

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')
bp.config = {}

# Spotify URLs
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = '{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)
USER_URL = '{}/{}'.format(SPOTIFY_API_URL, 'me')

# Server-side Parameters
CLIENT_SIDE_URL = 'http://127.0.0.1'
PORT = 5000
REDIRECT_URI = '{}:{}/auth/callback/q'.format(CLIENT_SIDE_URL, PORT)
SCOPE = 'playlist-modify-public playlist-modify-private'


@bp.record
def record_params(setup_state):
    """
    Overload record method to fetch the config parameters of the Flask app.
    This method is run when this blueprint is registered with the app.
    """
    app = setup_state.app
    bp.config = dict([(key, value) for (key, value) in app.config.items()])


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        auth_query_parameters = {
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE,
            'client_id': bp.config['CLIENT_ID']
        }

        # Spotify authorization
        url_args = '&'.join(['{}={}'.format(key, urllib.parse.quote(value))
                             for key, value
                             in auth_query_parameters.items()])
        auth_url = '{}/?{}'.format(SPOTIFY_AUTH_URL, url_args)
        return redirect(auth_url)

    # login page is shown when the user initially navigates to auth/login
    return render_template('auth/login.html')


@bp.route('/callback/q')
def callback():
    """
    After the user accepts, or denied the request,
    the Spotify Accounts service redirects the user back to the specified REDIRECT_URI
    """
    # check if Spotify authorization failed
    error = request.args.get('error')

    if error is not None:
        # error is shown to the user if authentication fails
        flash(error)
        # show the login page again if there was authentication error
        return render_template('auth/login.html')

    # request refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }
    base64encoded = base64.b64encode('{}:{}'.format(bp.config['CLIENT_ID'], bp.config['CLIENT_SECRET']).encode()).decode()
    headers = {'Authorization': 'Basic {}'.format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_type = response_data['token_type']
    expires_in = response_data['expires_in']

    # store tokens in the session
    session.clear()
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['token_type'] = token_type
    session['expires_in'] = expires_in

    # also get relevant user info
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    user_response = requests.get(USER_URL, headers=headers).json()
    session['user_id'] = user_response['id']

    return redirect(url_for('main.index'))


@bp.before_app_request
def load_logged_in_user():
    """
    If an access token is stored in the session, store token on g.token;
    If there is no access token, or if the token doesn't exist, g.token will be None
    """
    g.token = session.get('access_token')


@bp.route('/logout')
def logout():
    # remove the user id from the session
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    This decorator returns a new view function that wraps the original view it's applied to.
    The new function checks if an access token is loaded and redirects to the login page otherwise.
    If a token is loaded, the original view is called and continues normally.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.token is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
