from flask import Flask, request, render_template, url_for
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@app.route('/loging/', methods=['GET', 'POST'])
def loging():
    return render_template('loging.html')


@app.route('/help')
def helper():
    return 'this is help page'


@app.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_404.html', title="Page not found")



if __name__=='__main__':
    app.run(host='localhost',debug=True)
