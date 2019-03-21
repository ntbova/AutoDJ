import os

from flask import Flask
from flask import session


def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed on
        app.config.from_object(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return session.get('refresh_token')

    from .views import auth
    app.register_blueprint(auth.bp)

    from .views import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app
