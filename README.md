# On_the_Line_Forum
On the Line forum is a highly secure proposed way of handling an online forum. The code is kept at a minimum to only show how secure functions are setup and user functionality is kept at a minimum.

## Project setup

**Prerequisites:**
* python3
* pip3
* Unix/linux - ***If you are developing on windows you are on your own.***
* python3-venv
**Clone the project to your desired location**

* `git clone (...)`

**Create a python virtual environment in /backen/venv**

* `cd backend`

* `python3 -m venv venv`

* `virtualenv venv`

* `. venv/bin/activate`

**Install the required packages from requirements in the virtual environment**
* pip install -r requirements.txt

**You should be all set up to work on the project**

To run the project:
`cd` to the root directory og the project, then set environment variables for development and specify the app:
`export FLASK_ENV=development`,
`export FLASK_APP=backend/src/__init__.py`
Then run:
You should initialize the database before you run the application to get all the necessary tables.
`flask init-db`, then do:
`flask run`


## Working with mysql in python
Documentation can be found here: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

Example packages used:

```Python3
import mysql.connector
from mysql.connector import errorcode
```

### Setting up your development environment with mariadb
If you are using MacOS check out this guide: https://ellestad1995.github.io/legendary-adventure/#/macOS/devenvironment

If you are on other UNIX environment see this guide:
https://www.linode.com/docs/databases/mariadb/mariadb-setup-debian/

And again: If you are on Windows, just install Debian or some UNIX system.

### Project specific setup:

* Create user:

  Log in with root account. Either using `sudo mysql` or `mysql -u root -p`, then make the user:

   `CREATE USER 'tom'@'localhost' IDENTIFIED BY 'jerry';`
