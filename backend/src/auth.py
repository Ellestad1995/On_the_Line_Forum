import functools
import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents this repo / this project. And we important the get_db function.
from .db import get_db

# The blueprint /auth will represent the endpoints starting with /auth
# See the endpoint csv file for what is included.
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    authorized = session.get('auth_cookie')
    if authorized is None:
        g.user = None
    else:
        cnx = get_db()
        cursor = cnx.cursor()
        g.user = cursor.execute('SELECT * FROM users WHERE id = ? ', ())




# /auth
@bp.route('/', methods=['GET'])
def login():
    """
        Registers a new user. Provides a form so the
        user can enter email, passord.
    """
    if request.method == 'GET':
        db = get_db()
        return render_template('base.html')

@bp.route('/profile', methods=['GET'])
def profile():
    """
    Display a users information
    """
    if request.method == 'GET':
        return render_template('base.html')

# /auth/user POST
# Post request for creating a new user
# TODO: Implement this


# /auth/user DELETE
# Delete a user
# TODO: Implement this

# /auth/user/:userid/ GET
# GET
# TODO: Implement this
