import functools
import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

bp = Blueprint('threads', __name__, url_prefix='/categories')

# /categories
@bp.route('/', methods=['GET'])
def name():
    return "Test of threads"

# /:categories/:threadid/