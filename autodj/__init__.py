import os
import urllib.parse
import datetime

from flask import Flask, render_template, redirect, url_for, session


def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed on
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        access_token = session.get('access_token')
        expiration = session.get('expiration')
        if access_token is None or expiration is None or (expiration is not None and datetime.datetime.now() >= expiration):
            client_id = 'dee71a70880043d799fb3beeb6622a9d' # TODO: single point of control for this, ***also located in auth.py***
            response_type = 'code'
            redirect_uri = 'http://127.0.0.1:5000/auth/login' # TODO: single point of control for this, ***also located in auth.py***
            scope = 'playlist-modify-public'
            auth_url = 'https://accounts.spotify.com/authorize?client_id=' + client_id + '&response_type=' + response_type + '&redirect_uri=' + urllib.parse.quote(redirect_uri) + '&scope=' + urllib.parse.quote(scope)
            return redirect(auth_url)
        
        # there is an access_token, user is logged in
        return render_template('demo.html')

    from .views import auth
    app.register_blueprint(auth.bp)
    from .views import playlist
    app.register_blueprint(playlist.bp)

    return app
