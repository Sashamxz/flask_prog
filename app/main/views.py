from calendar import calendar
from flask import render_template, request, redirect, url_for, flash, make_response, session, current_app
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user, logout_user
from . import main
from .. import db
from .forms import PostForm
from ..models import Post, Subscribe , User
from flask_security import login_required
from werkzeug.security import check_password_hash, generate_password_hash


# Обработчик подписки на новости
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        if len(request.form.get('email')) > 3:
            sub_cl = request.form.get('email')
            param = None

            # запись тех, кто подписался в файл
            # with open ('client.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{sub_cl} \n ' )
            #     flash('You were successfully subscribe !')

            #проверка на наличие подписки    
            if Subscribe.query.filter(Subscribe.email == f'{sub_cl}').all():
                flash(" You are already subscribed ")
                param = True
                return render_template('block.html', param=param)

            try:
                subscribe_m = Subscribe(email=sub_cl)
                db.session.add(subscribe_m) #Запись в базу данних 
                db.session.commit()
                param = True
                flash('You were successfully subscribe !')
                return render_template('block.html', param=param)

            except BaseException:
                print('db error')
        else:
            flash(u'Something wrong! \
            Confirm your entries', 'error')

    return render_template('block.html')


# Создание поста
@main.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except BaseException:
            print('error db.add 498e238e')

        return redirect(url_for('main.index'))

    form = PostForm()
    return render_template('create_post.html', form=form)


# Редактирование поста
@main.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('main.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('edit_post.html', post=post, form=form)


# страница блога
@main.route('/blog', methods=['GET', 'POST'])
def index():
    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(
            q) | Post.body.contains(q)).all()
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)

    return render_template('index.html', posts=posts, pages=pages)

# главная страница
@main.route('/')
def home_view():
    return render_template('block.html')


# Посто по слагу
@main.route('/<slug>/')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('post_d.html', post=post)


# Старница авторизации пользователей



@main.route('/help')
def helper():
    return 'this is help page'





@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=('Register'),
                           form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=('Sign In'), form=form)



@main.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


# страница не найдена 404
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'), 404
