from flask import Flask, request, render_template, url_for
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:123@localhost/test.db'
db = SQLAlchemy(app)
app.config.from_object(__name__)






class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
 
    def __init__(self, text,tags):
        self.text = text.stript()
        self.tags = [
           Tag(text=tag.strip()) for tag in tags.split(',')
        ]
     

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)
    
    message_id = db.Column(db.Integer, db.ForeignKey('massage.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

db.create_all()



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
    app.run(host='11.0.0.28',debug=True)
