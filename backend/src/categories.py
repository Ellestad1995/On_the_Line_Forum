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
@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    categories = db.execute(
        'SELECT id, displayname'
        ' FROM category'
        ' ORDER BY id'
    ).fetchall()

    return render_template('category/index.html', categories=categories)

#Return different pages whether the user is authenicated or not


# /categories/:name/
