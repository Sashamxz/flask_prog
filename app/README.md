

Start flask project:
Open terminale:

$ cd flask-prog
$ python -m venv env
$ source env/bin/activate  #for  Windows user - env\Scripts\activate
(venv)$ pip install -r requirements.txt

# Flask-Migrate create database
(venv)$ flask db upgrade

# Pre deploy, eg. insert roles
(venv)$ flask deploy

# create back-end/.env file, like this
FLASK_APP=madblog.py
FLASK_DEBUG=1

(venv)$ flask run