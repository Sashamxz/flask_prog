# flask_proj
Simple blog, powered by best framework in the World - Flask.

Install OS Packages
You will at least need the python development package though there 
might be more packages required depending on your setup.

```
$ sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
```
Python Packages using pip and installing a virtual environment.

```
$ sudo apt install -y python3-venv

$ python3 -m venv env

$ source env/bin/activate

(env)$ pip install -r requirements.txt

(env)$ export FLASK_APP=flask_proj.py

(env)$ python flask_proj.py runserver
```
