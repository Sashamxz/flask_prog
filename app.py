from flask import Flask, request, render_template

app = Flask(__name__)


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
    app.debug = True 
    app.run()    