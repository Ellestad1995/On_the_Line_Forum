import functools
import click
import datetime
from .objects.UserClass import User
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

bp = Blueprint('threads', __name__, url_prefix='/thread')

# ========
# Checking if the request is a logged in user
# =========
# Using the session object we can get read cookies sent over the network
# If no cookie/token is found then the user is not logged in.
#
@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from
    the database into ``g.user``.
    """

    authorized = session.get('access_token')
    click.echo("What is wrong: {}".format(authorized))
    if authorized is None:
        g.user = None
    else:
        cnx = get_db()
        cursor = cnx.cursor(dictionary=True)
        query = 'SELECT id, username, groupid, email, tokentimestamp FROM user WHERE token = %s '
        cursor.execute(query, (authorized,))
        row = cursor.fetchone()
        if row is not None:
            g.user = User(row)
            #g.user.dump()
        else:
            g.user = None
            click.echo("No user was found. Return to homepage")

# /:categoryid
@bp.route('/<categoryid>/', methods=['GET'])
def showthreads(categoryid):
    cnx = get_db()
    cursor = cnx.cursor()
    results = cursor.execute("SELECT id, threadname FROM thread WHERE categoryid = %s", (categoryid,))
    threads = cursor.fetchall()
    click.echo(str(threads))
    return render_template("thread/index.html", categoryid=categoryid, threads=threads)

# ========
# Posting a new thread
# =========
# Gets title and content from the user and posts a new thread with the title,
# The content of the thread will be put in the first post.
#
@bp.route('/<categoryid>/', methods=['POST'])
def create_newthread(categoryid):
    if g.user is not None:
        title=str(escape(request.form['title']))
        content=str(escape(request.form['content']))
        click.echo(title + content)
        if title and content:
            cnx=get_db()
            cursor=cnx.cursor()
            timestamp=format(datetime.datetime.now())
            cursor.execute("INSERT INTO `thread` (`threadname`, `categoryid`) VALUES (%s, %s)", (title, categoryid))
            cnx.commit()
            threadid=cursor.lastrowid
            cursor.execute("INSERT INTO `post` (`title`, `content`, `timestamp`, `userid`, `threadid`) VALUES (%s, %s, %s, %s, %s)", (title,content,timestamp,g.user.id,threadid))
            cnx.commit()
        return redirect("/post/"+categoryid+"/"+str(threadid)+"/")
    else:
        click.echo("Log in to post a new thread.")

# ========
# Deleting a thread or all threads by a user in a thread
# =========
# Deletes entire thread if admin,
# Deletes all posts by that particular user if regular user
#
@bp.route('/delete/<threadid>', methods=['POST'])
def deleteThread(threadid):
    cnx=get_db()
    cursor=cnx.cursor()
    if g.user.isAdmin():
        cursor.execute("DELETE FROM post WHERE threadid = %s", (threadid,))
        cnx.commit()
        cursor.execute("DELETE FROM thread WHERE id = %s", (threadid,))
        cnx.commit()
        return redirect("/")
    elif g.user is not None:
        cursor.execute("DELETE FROM post WHERE threadid = %s AND userid = %s", (threadid, g.user.id,))
        cnx.commit()
        return redirect("/")
