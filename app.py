from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name='Admin')


@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    if username == 'root' and password == 'pass':
        message = "Correct username and password"
    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message)


@app.route('/help')
def helper():
    return 'this is help page'


@app.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


if __name__ == '__main__':
    app.debug = True
    app.run()
