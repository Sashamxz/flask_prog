from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    print(i)
    return 'Hello, World!'

@app.route('/help')
def helper():
    return 'this is help page'

@app.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)





if __name__=='__main__':
    app.debug = True 
    app.run()    