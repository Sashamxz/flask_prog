from flask import Flask, request, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db= SQLAlchemy



@app.route('/')
def index():
    return render_template('index.html', name='Admin')


@app.route('/help')
def helper():
    return 'this is help page'


@app.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


if __name__=='__main__':
    manager.run()
