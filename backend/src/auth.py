import functools
import click
import mysql.connector
import re
import secrets
from .objects.UserClass import User
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash
import itsdangerous

# Obviously we need database access in functions here
# the '.' represents this repo / this project. And we important the get_db function.
from .db import get_db

# The blueprint /auth will represent the endpoints starting with /auth
# See the endpoint csv file for what is included.
bp = Blueprint('auth', __name__, url_prefix='/auth')


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

# /auth/register
# ==========
# User registration
# ==========
# For a GET request we want to deliver the form so the user can register
# For a POST request we will read the field the user entered and register the user.
#
# Password hashing method ref: http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.security.generate_password_hash

@bp.route('/register', methods=('GET','POST'))
def createUser():
    """
        Registers a new user. Provides a form so the
        user can enter email, passord.
    """
    if request.method == 'GET':
        """
        Render a signup page
        """
        return render_template('auth/index.html', title='register')

    elif request.method == 'POST':

        """
            Read the form data
            Verify that we can get and all the data - tampering is a script kiddies game
            Checklist:
            * equal passwords
            * Password strength
            * is email used
            * accepted terms
        """


        email = request.form['email']
        username = request.form['username']
        password = request.form['secretPassword']
        verifyPassword = request.form['verifySecretPassword']
        acceptTerms = request.form['acceptTerms']
        #click.echo("User gave us: `{}`".format([email,username,password,acceptTerms]))
        error = None

        if not email and isEmail(email) is False:
            error = "A valid email address is required"
        elif not re.match(r'.{10,}', password):
            error = "Password needs to be 10 or longer"
        elif not username:
            error = "A username is required"
        elif not password:
            error = "Obviously you need a password"
        elif not verifyPassword:
            error = "We need you to type your password again"
        elif not password == verifyPassword:
            error = "Your passwords doesn't match"
        elif not acceptTerms:
            error = "We need you to accept the terms"
        elif acceptTerms == False:
            error = "You must accept the terms"

        cnx = get_db()
        cursor = cnx.cursor()

        # Check for existing username and email
        query = 'SELECT id FROM user WHERE username = %s OR email = %s'
        cursor.execute(query, (username,email))

        if cursor.fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            # Nothing to worry about
            # Its all good
            # Create the user
            # werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=10)
            click.echo("error is None")
            try:
                click.echo("Try")
                insert = ('INSERT INTO user'
                        '(username, email, password)'
                        'VALUES (%s, %s, %s)')
                cursor.execute(insert,(username, email, password_hash))
                newUser = cursor.lastrowid
                cnx.commit()
                return redirect(url_for('auth.login'))
            except mysql.connector.Error as err:
                # TODO: Specific error handling
                click.echo("Unknown error: {} ".format(err))
                error = "Something went wrong"
            else:
                click.echo("Something went wrong...")

    flash(error)
    return redirect(url_for('auth.createUser'))

# auth/
# =======
# Enables the user to login
# =======
@bp.route('/', methods=['GET', 'POST'])
def login():
    """
    render a sign in page
    """
    if request.method == 'GET':
        
        if g.user is None:
            return render_template('auth/login.html', title='login')
        else:
            return redirect(url_for('categories.index'))


    elif request.method == 'POST':
        """
            Read form data
            Check username presence
            Check email presence
            Check password presence
            Check if username exists
            Check if password is correct
            login :O

        """

        username = request.form['username']
        password = request.form['secretPassword']

        db = get_db()
        cnx = db.cursor()

        boolMail = isEmail(username)
        if boolMail:
            cnx.execute(
                    "SELECT email, password FROM user WHERE email = %s", (username,))
        elif not boolMail:
            cnx.execute(
                    "SELECT username, password FROM user WHERE username = %s", (username,))

        row = cnx.fetchone()
        error = None
        if not username:
            error = "A username/email is required"
        elif not password:
            error = "A password is required"
        elif row == None:
            error = "Username/email or password is incorrect"
        elif not check_password_hash(row[1], password):
            error = "Password is incorrect"
        else: 
            uniqueToken = secrets.token_hex(128)
            #uniqueToken = TimestampSigner(randomString)
            try:
                if boolMail:
                    cnx.execute(
                            'UPDATE user SET token = %s WHERE email = %s', (uniqueToken, username,))
                elif not boolMail:
                    cnx.execute(
                            'UPDATE user SET token = %s WHERE username = %s', (uniqueToken, username,))
                db.commit()

            except mysql.connector.Error as err:
                # TODO: Error handling
                click.echo("Unknown error: {} ".format(err))

            session['access_token'] = uniqueToken

            #redirect to a success page
            return redirect(url_for('categories.index'))
        flash(error)
        return redirect(url_for('auth.login'))


@bp.route('/profile', methods=['GET'])
def profile():
    """
    Display a users information
    """
    if request.method == 'GET':
        return render_template('base.html')


# /auth/user/:userid/ DELETE
# Delete a user
# TODO: Implement this
@bp.route('/user', methods=['DELETE'])
def deleteUser():
    if request.method == 'DELETE':
        db = get_db()
        cnx = db.cursor()

        authorized = session.get('access_token')
        try:
            if authorized is None:
                cnx.execute('SELECT username FROM user WHERE token = %s', (authorized,))
                row = cursor.fetchone()
                username = row[0]
                cnx.execute('DELETE FROM user WHERE username = %s', (username,))
            #elif isAdmin():
            else:
                click.echo("Not authorized to delete")
            db.commit()
        except mysql.connector.Error as err:
            # TODO: specific error handling
            click.echo("YO YO YO: {}".format(err))

# /auth/user/logout
# logout GET
#@bp.route
#def logout():
#    if request.method == 'GET':
        

# /auth/user/:userid/ GET
# GET
# TODO: Implement this


# Checks if provided string is an email
def isEmail(txt):
    garbage = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", txt)
    if garbage is not None:
        return True
    return False
