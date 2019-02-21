import functools
import requests
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        error = request.args.get('error') # if there is an error
        # not sure if this is correct error handling
        if error is not None:
            flash(error)

        code = request.args.get('code') # auth code that can be exchanged for access token
        url = 'https://accounts.spotify.com/api/token'
        grant_type = 'authorization_code'
        redirect_uri = 'http://127.0.0.1:5000/auth/login'
        client_id = 'dee71a70880043d799fb3beeb6622a9d' # not secure
        client_secret = 'd1f58af1e702408082984a99ec18f5f6' # not secure

        data = {
            'code': code,
            'grant_type': grant_type,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(url, data=data).json()
        access_token = response['access_token']
        expires_in = response['expires_in']
        expiration = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        refresh_token = response['refresh_token'] # can repeat steps above with this as 'code' to get new access token once expired

        # not sure if this is right
        session.clear()
        session['access_token'] = access_token
        session['expiration'] = expiration
        session['expires_in'] = expires_in # should probs extrapolate this into a Date\
        session['refresh_token'] = refresh_token

        # also get relevant user info
        user_url = "https://api.spotify.com/v1/me"
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        user_response = requests.get(user_url, headers=headers).json()
        session['user_id'] = user_response['id']

        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = 'error'
        user = None

        # todo: login with spotify api

        if error is None:
            # user's id is stored in a new session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        # error is shown to the user if authentication fails
        flash(error)

    # login page is shown when the user initially navigates to auth/login or there was authentication error
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, store user on g.user;
    If there is no user id, or if the id doesn't exist, g.user will be None
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        pass  # todo: get user from spotify


@bp.route('/logout')
def logout():
    # remove the user id from the session
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    This decorator returns a new view function that wraps the original view it's applied to.
    The new function checks if a user is loaded and redirects to the login page otherwise.
    If a user is loaded, the original view is called and continues normally.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
