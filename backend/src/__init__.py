import os
import datetime
from flask import Flask

from .db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # TODO: Needs ip address of mysql database
    app.config.from_mapping(
        SECRET_KEY='ontheline',
        DATABASE='127.0.0.1:6969',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database init and setup.
    from . import db
    db.init_app(app)

    # Adding blueprints here. Use the same import line
    from . import auth, categories, posts, threads
    app.register_blueprint(auth.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(threads.bp)

    # The index page redirects to categories index()
    app.add_url_rule('/', endpoint='categories.index')

    # Gives the cookie a lifetime
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
    #app.config['SESSION_COOKIE_HTTPONLY'] = False
    #app.config['SESSION_COOKIE_SECURE'] = True
    return app
