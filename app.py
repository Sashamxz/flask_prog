from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/help ')
def helper():
    return 'this is help page'

if __name__=='__main__':
    app.debug = True 
    app.run()    