
from flask import render_template, request, redirect, url_for, flash, make_response, session, current_app
from flask_login import login_required, login_user,current_user, logout_user
from . import main
from .. import db
from .forms import PostForm
from ..models import Post
from ..calendar import  show_calendar
# from .forms import ContactForm, LoginForm
# from .utils import send_mail



@main.route('/create', methods=['POST','GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('error db.add 498e238e')    

        return redirect( url_for('main.index'))

    form = PostForm()
    return render_template('create_post.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:    
        posts = Post.query.order_by(Post.created.desc())
    
    return render_template('index.html',posts=posts)



@main.route('/', methods=['GET'])
def date_today():
    show_calendar()
    return render_template('index.html')

@main.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('post_d.html', post = post)



@main.route('/loging/', methods=['GET', 'POST'])
def loging():
    return render_template('loging.html')


@main.route('/help')
def helper():
    return 'this is help page'


@main.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'),404
