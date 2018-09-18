import os

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
    from . import auth
    app.register_blueprint(auth.bp)
    # Need blueprint for categories
    # Need blueprint for threads

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "hello verden"

    return app
