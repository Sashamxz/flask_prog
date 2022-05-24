from distutils.log import error
from flask import render_template, request, redirect, url_for, flash, make_response, session, current_app
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user, logout_user
from . import main
from .. import db
from .forms import PostForm ,CommentForm
from ..models import Post, Subscribe , User , Comment , Permission
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
    if current_user.can(Permission.WRITE):    
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
    flash('Доступ ограничен')
    return redirect(url_for('main.index'))


# Редактирование поста
@main.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    if current_user.can(Permission.MODERATE):
        post = Post.query.filter(Post.slug == slug).first()

        if request.method == 'POST':
            form = PostForm(formdata=request.form, obj=post)
            form.populate_obj(post)
            db.session.commit()
            return redirect(url_for('main.post_detail', slug=post.slug))

        form = PostForm(obj=post)
        return render_template('edit_post.html', post=post, form=form)
    flash('Доступ ограничен')
    return redirect(url_for('main.index')) 




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
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)

    return render_template('index.html', posts=posts, pages=pages)


@main.route('/create-comment/<slug>', methods=['GET', 'POST'])
@login_required
def create_comment(slug):
    
    post_id = Post.query.filter(Post.slug == slug).first().id
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(body=text, author=current_user._get_current_object(), post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('main.post_detail', slug=slug)) 







@main.route("/delete-comment/<slug>")
@login_required
def delete_comment(slug):
    
    comment = Comment.query.filter(Comment.author==current_user).all()
    
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('main.post_detail', slug=slug))     

# главная страница
@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home_view():
    
    return render_template('block.html')


# Посто по слагу
@main.route('/<slug>/')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    
    return render_template('post_d.html', post=post)


@main.route('/help')
def helper():
    return 'this is help page'





@main.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)

