import functools
import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

bp = Blueprint('threads', __name__, url_prefix='/')

# /:categoryid
@bp.route('/<categoryid>', methods=['GET'])
def showthreads(categoryid):
    cnx = get_db()
    cursor = cnx.cursor()
    cursor.execute("select id, threadname FROM thread WHERE categoryid = " + categoryid)
    threads = cursor.fetchall()	
    click.echo(str(threads))
    return render_template("thread/index.html", threads=threads)

