import functools
import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

bp = Blueprint('categories', __name__, url_prefix='/categories')

# /
@bp.route('/categories', methods=['GET'])
def index():
    cnx = get_db()
    cursor = cnx.cursor()
    cursor.execute("select id, displayname FROM category")
    categories = cursor.fetchall()
    click.echo(str(categories))
    return render_template('category/index.html', categories=categories)

#Return different pages whether the user is authenicated or not


# /categories/:name/
