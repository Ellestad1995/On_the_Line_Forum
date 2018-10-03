# On_the_Line_Forum
On the Line forum is a highly secure proposed way of handling an online forum. The code is kept at a minimum to only show how secure functions are setup and user functionality is kept at a minimum.


## Usage with docker
If you want to run this app in a docker enviroment, you can follow the guide on the [wiki](https://github.com/Ellestad1995/On_the_Line_Forum/wiki/Usage-with-docker-compose)<br>

## Project setup
For reference: [Flask install guide](http://flask.pocoo.org/docs/1.0/installation/#installation)


**Prerequisites:**
* python3
* pip3
* FreeBSD,Unix/linux, Windows
* python3-venv

**Clone the project to your desired location**

* `git clone (...)`

**Create a python virtual environment in /backen/venv**

* `cd backend`

* `python3 -m venv venv`

* `source venv/bin/activate` - This is how you enable the virtual environment

The windows way:

* Goto the backend directory
* `python -m venv venv`
* `venv\Scripts\activate` -  This is how you enable the virtual environment

**Install the required packages from requirements in the virtual environment**
* pip3 install -r requirements.txt

The windows way:

* `pip install -r requirements.txt`

This will install Flask and the required dependences and other packages.

**You should be all set up to work on the project**

## To run the project:
**You must be in the virtual environment to use flask**

Set the environment variables so Flask know that we are developing and so it knows where the project is:

* `cd` to the root directory of the project, then set environment variables for development and specify the app:

* `export FLASK_ENV=development`

* `export FLASK_APP=backend/src/__init__.py`

* `export FLASK_DB=127.0.0.1` or `export FLASK_DB=db` if on docker.

The windows way:

* `(venv) E:\Bibliotek\Dokumenter\On_the_Line_Forum\backend>set FLASK_APP=src`
* `(venv) E:\Bibliotek\Dokumenter\On_the_Line_Forum\backend>set FLASK_ENV=development`

You should initialize the database before you run the application to get all the necessary tables.

`flask init-db` - Don't do this before setting up the db. see next section.

`flask dummy` - To populate the database with dummy data. See dummyData.sql

Use `flask run` in the virtual environment environment.
You should now see something like this:
```
(venv) Star-Lord-MBP:backend joakimellestad$ flask run
 * Serving Flask app "src/__init__.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```
If you now browse to `http://127.0.0.1:500/hello` you will se a dummy page. That is the only page currently configured.



### Setting up your development environment with mariadb

**You need mariadb database and mysql-client for connecting to the mariadb database.(Yeah..it's confusing)**

* If you are using MacOS check out this guide: https://docs.nivlheim.cloud/legendary-adventure/#/macOS/devenvironment

* If you are on other UNIX environment see this guide:
https://www.linode.com/docs/databases/mariadb/mariadb-setup-debian/

* Windows users can check out this https://mariadb.com/kb/en/library/installing-mariadb-msi-packages-on-windows/

### Project specific setup:

* Create user:

  Log in with root account. Either using `sudo mysql` or `mysql -u root -p`, then make the user:

   `CREATE USER 'tom'@'localhost' IDENTIFIED BY 'jerry';`

* Grant the user privileges for creating db. Only for use in development. This ensures that we can generate a new database with `flask init-db` when we need a fresh db.

  `grant all privileges on *.* to 'tom'@'localhost';`




## Working with mysql in python
Documentation can be found here:
* https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
* https://mariadb.com/resources/blog/how-connect-python-programs-mariadb

Example packages used:

 ```Python3
 import mysql.connector
 from mysql.connector import errorcode
 ```


## Writing comments/documentation
**The project uses reStructuredText/sphinx to generate the documentation**
* http://www.sphinx-doc.org/en/master/usage/quickstart.html
* https://docs.python-guide.org/writing/documentation/
* https://devguide.python.org/documenting/#restructuredtext-primer
