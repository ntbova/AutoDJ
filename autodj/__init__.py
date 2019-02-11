import os

from flask import Flask, render_template, redirect, url_for


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
        return redirect(url_for('auth.login'))

    from .views import auth
    app.register_blueprint(auth.bp)

    return app
