import functools
import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

# The blueprint /auth will represent the endpoints starting with /auth
# See the endpoint csv file for what is included.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# /auth
@bp.route('/', methods=['GET'])
def loginCheck():
    """
        Registers a new user. Provides a form so the
        user can enter email, passord.
    """
    if request.method == 'GET':
        db = get_db()
        click.echo("Seems like we could do it this way")

# /auth/user POST
# Post request for creating a new user
# TODO: Implement this


# /auth/user DELETE
# Delete a user
# TODO: Implement this

# /auth/user/:userid/ GET
# GET
# TODO: Implement this
