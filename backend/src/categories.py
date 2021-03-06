import functools
import click
from flask import (
    Blueprint, flash, g, flash ,redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Obviously we need database access in functions here
# the '.' represents __init__.py / this project. And we important the get_db function.
from .db import get_db
from .objects.UserClass import User
bp = Blueprint('categories', __name__, url_prefix='/categories/')

@bp.route('/', methods=['GET'])
def index():
    cnx = get_db()
    cursor = cnx.cursor()
    cursor.execute("select id, displayname FROM category")
    categories = cursor.fetchall()
    #TODO: check to see if current user is admin, and pass it as a paramter to the template
    try:
        adminuser = g.user.isAdmin()
    except:
        adminuser = False
    return render_template('category/index.html', categories=categories, adminuser=adminuser)

@bp.route('', methods=['POST'])
def add_entry():
    cnx = get_db()
    cursor = cnx.cursor()
    newcategory = request.form["new"]
    deletecategory = request.form["delete"]

    if newcategory:
        if len(newcategory) < 30:
            cursor.execute("SELECT displayname FROM category where displayname = %s", (newcategory,))
            data = cursor.fetchone()
            if data is None:
                cursor.execute("INSERT INTO category (displayname) VALUES (%s)", (newcategory,))
                cnx.commit()
            else:
                flash("Name must be unique")
        else:
            flash("Name must be less than 30 chars")

    if deletecategory:
        cursor.execute("SELECT displayname FROM category where displayname = %s", (deletecategory,))
        data = cursor.fetchone()
        if data is not None:
            cursor.execute("DELETE FROM category WHERE displayname = %s", (deletecategory,))
            cnx.commit()
        else:
            flash("What want you delete does not exsist")

    return redirect("/")
