from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/loging/', methods=['GET', 'POST'])
def index():
    return render_template('loging.html')


@app.route('/help')
def helper():
    return 'this is help page'


@app.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


if __name__=='__main__':
    app.run(host='192.168.1.22',debug=True)
