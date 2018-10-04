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
    results = cursor.execute("SELECT id, threadname FROM thread WHERE categoryid = %s", (categoryid,))
    threads = cursor.fetchall()	
    click.echo(str(threads))
    return render_template("thread/index.html", threads=threads)

# /:categories/r/:threadid/
# =========
# Show posts in a thread
# =========
# GET requests shows all posts and their information in that thread

@bp.route('/threadid', methods=['GET'])
def showPosts():
        cnx = get_db()
        cursor = cnx.cursor()
        results = cursor.execute("SELECT * FROM post WHERE threadid = %s", (threadid,))
        posts = cursor.fetchall()
        click.echo(str(posts))
        return render_template("post/index.html", posts=posts)

