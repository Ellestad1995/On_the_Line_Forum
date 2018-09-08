import click
import mysql.connector
from mysql.connector import errorcode
from flask import current_app, g
from flask.cli import with_appcontext

DB_NAME='onthelinedb'
# Reference for mysql: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
# Get a couchdb session
# Returns the already established connection if it exists or tries to
# create a new one.
# Handles error for "access denied" and "unknown database"
def get_db():
    if 'db' not in g:
        try:
            cnx = mysql.connector.connect(user='tom', password='jerry',
                              host='127.0.0.1',
                              database=DB_NAME)
            g.db = cnx
            return g.db
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                click.echo("Connection failed! Check username and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                click.echo("Database does not exist")
            else:
                click.echo("Unknown error: {} ".format(err))
        else:
            cnx.close()
        # Don't bother continueing execution if connection to db cannot
        # be established. DB is life.
        exit(1)
    return g.db

# Closes session
def close_db(e=None):
    cnx = g.pop('db', None)

    if cnx is not None:
        cnx.close()

def init_db():
    cnx = get_db()
    cursor = cnx.cursor()
    with current_app.open_resource('schema.sql') as f:
        try:
            cursor.execute(f)
        except mysql.connector.Error as err:
            click.echo("Failed creating database: {}".format(err))
            exit(1)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    click.echo("init_app runs")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
