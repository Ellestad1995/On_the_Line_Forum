import functools
import click
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db

bp = Blueprint('posts', __name__, url_prefix='/')

# /:categoryid
@bp.route('/<categoryid>/<threadid>/', methods=['GET'])
def showthreads(threadid, categoryid):
    cnx = get_db()
    cursor = cnx.cursor()
    results = cursor.execute("SELECT title, content, threadid FROM post WHERE threadid = %s", (threadid,))
    posts = cursor.fetchall() 
    click.echo(str(posts))
    return render_template("post/index.html", posts=posts, categoryid=categoryid, threadid=threadid)

@bp.route('/<categoryid>/<threadid>/', methods=['POST'])
def create_newpost(threadid, categoryid):
    title=request.form['title']
    content=request.form['content']
    click.echo(title + content)
    #TODO: check if both fields have text in them, Insert into database
    if title and content:
        cnx=get_db()
        cursor=cnx.cursor()
        timestamp=format(datetime.datetime.now())
        #change userid to g.obj
        userid=int(1)
        cursor.execute("INSERT INTO `post` (`title`, `content`, `timestamp`, `userid`, `threadid`) VALUES (%s, %s, %s, %s, %s)", (title,content,timestamp,userid,int(threadid)))
        cnx.commit()
    return redirect("/"+categoryid+"/"+threadid+"/") 




