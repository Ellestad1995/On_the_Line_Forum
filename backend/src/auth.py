import functools
import click
import secrets
import mysql.connector
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

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
    authorized = session.get('token')
    if authorized is None:
        g.user = None
    else:
        cnx = get_db()
        cursor = cnx.cursor()
        row = cursor.execute(
        'SELECT id, username, groupid FROM user WHERE token = ? ', (authorized)
        ).fetchone()
        if row is not None:
            g.user = row



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
        if not email:
            error = "An email address is required"
        elif not username:
            error = "A username is required"
        elif not password:
            error = "Obviously you need a password"
        elif not verifyPassword:
            error = "We need you to type your password again"
        elif not password == verifyPassword:
            error = "Your passwords doesn't match"
            # TODO: Make this check client side.
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
        return render_template('auth/login.html', title='login')


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
        elif not ckeck_password_hash(row[1], password):
            #sjekk passord client side??
            #får feilmlding siden de dummydataen inneholder passord som ikke er hashet
            error = "Username/email or password is incorrect" 
        else:
            # TODO: Security? secrets only generates a hex string of 490 chars with this
            uniqueToken = secrets.token_hex(245)
            try:
                if boolMail:
                    cnx.execute(
                            'UPDATE user set token %s WHERE email = %s', (uniqueToken, username,))
                elif not boolMail:
                    cnx.execute(
                            'UPDATE user SET token = %s WHERE username = %s', (uniqueToken, username,))
                db.commit()

            except mysql.connector.Error as err:
                # TODO: Error handling
                click.echo("Unknown error: {} ".format(err))

            #redirect to a success page
            return redirect(url_for('/'))
        flash(error)
        return redirect(url_for('auth.login'))


@bp.route('/profile', methods=['GET'])
def profile():
    """
    Display a users information
    """
    if request.method == 'GET':
        return render_template('base.html')

# /auth/user POST
# Post request for creating a new user
# TODO: Implement this




# /auth/user DELETE
# Delete a user
# TODO: Implement this
#@bp.route('/user', methods=['DELETE'])
#def deleteUser():



# /auth/user/:userid/ GET
# GET
# TODO: Implement this

# Checks if provided string is an email
def isEmail(txt):
    garbage = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", txt)
    if garbage is not None:
        return True
    return False


