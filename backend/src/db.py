import click
import mysql.connector
from mysql.connector import errorcode
from flask import current_app, g
from flask.cli import with_appcontext

DB_NAME='onthelinedb'
# Reference for mysql: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
# Returns the already established connection if it exists or tries to
# create a new one.
# Handles error for "access denied" and "unknown database"
def get_db():
    if 'db' not in g:
        try:
            click.echo("Trying to connect")
            cnx = mysql.connector.connect(user='tom', password='jerry',
                              host='127.0.0.1',
                              database=DB_NAME)
            g.db = cnx
            return g.db
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                click.echo("Connection failed! Check username and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                click.echo("Database does not e     xist")
            else:
                click.echo("Unknown error: {} ".format(err))
        else:
            cnx.close()
        # Don't bother continueing execution if connection to db cannot
        # be established. DB is life.
        exit(1)
    click.echo("Using existing connection")
    return g.db

def init_db():
    """
        The purpose of this function is to initialize the database.
        The database should already exists, but we will create the tables.
    """
    cnx = get_db()
    cursor = cnx.cursor()
    with current_app.open_resource('schema.sql') as f:
        try:
            cursor.execute(f.read().decode('utf8'))
        except mysql.connector.Error as err:
            click.echo("Failed creating database: {}".format(err))
            exit(1)

def insert_dummy():
    """
    This function fills a existing databse with dummy data that is red from dummyData.sql

    """
    cnx = get_db()
    cursor = cnx.cursor()
    with current_app.open_resource('dummyData.sql', 'r') as f:
        try:
            for line in f.readlines():
                click.echo("line: {}".format(line))
                cursor.execute(line)
        except mysql.connector.Error as err:
            click.echo("Failed inserting dummy data: {}".format(err))
            exit(1)
    cnx.commit()
    cursor.close()

# Closes session
def close_db(e=None):
    click.echo("close_db")
    cnx = g.pop('db', None)
    if cnx is not None:
        cnx.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('dummy')
@with_appcontext
def insertDummyData():
    """Insert dummy data"""
    insert_dummy()
    click.echo("Done inserting dummy data")

@click.command('fresh-db')
@with_appcontext
def fresh_db():
    """ One command to rule them all """
    click.echo("Runs: init-db")
    init_db()
    click.echo("Runs: insert dummy")
    insert_dummy()
    click.echo("Created a fresh database. Keep on the good work!!")


def init_app(app):
    click.echo("init_app runs")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insertDummyData)
    app.cli.add_command(fresh_db)
