from distutils.log import error
from flask import render_template, request, redirect, url_for, flash, make_response, session, current_app 
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user, logout_user
from . import main
from .. import db
from .forms import PostForm ,CommentForm
from ..models import Post, Subscribe , User , Comment , Permission , Like
from werkzeug.security import check_password_hash, generate_password_hash






# Обробник підписки на новини 
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        if len(request.form.get('email')) > 3:
            sub_cl = request.form.get('email')
            param = None

            # запис тих, хто підписався в файл
            # with open ('client.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{sub_cl} \n ' )
            #     flash('You were successfully subscribe !')

            #перевірка наявності підписки     
            if Subscribe.query.filter(Subscribe.email == f'{sub_cl}').all():
                flash(" You are already subscribed ")
                param = True
                return render_template('block.html', param=param)

            try:
                #Запис в базу данних  
                subscribe_m = Subscribe(email=sub_cl)
                db.session.add(subscribe_m) 
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


# Створення поста
@main.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if current_user.can(Permission.WRITE):    
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            user_id = current_user.id
            try:
                post = Post(title=title, body=body, author_id=user_id)
                db.session.add(post)
                db.session.commit()
            except BaseException:
                print('error db.add 498e238e')

            return redirect(url_for('main.index'))

        form = PostForm()
        return render_template('create_post.html', form=form)
    flash('Доступ ограничен')
    return redirect(url_for('main.index'))


# Редагування поста 
@main.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    #перевірка доступу для редагування
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




# сторінка блога
@main.route('/blog', methods=['GET', 'POST'])
def index():
    #пошук !тільки серед постів!   за допомогою  аргумента "search?q=" 
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



#Створення  коментарів під постом 
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
            #запис коментаря в базу данних
            comment = Comment(body=text, author=current_user._get_current_object(), post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('main.post_detail', slug=slug)) 






#Видалення коментаря
@main.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    
    slug = Post.query.filter(Post.id==comment.post_id).first().slug
    
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author_id and current_user.id != comment.post.author_id:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.post_detail', slug=slug))
    return redirect(url_for('main.index'))    
  

# Головна сторніка новин 
@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home_view():
    
    return render_template('block.html')


# Детальна інформація про пост з коментарями
@main.route('/<slug>/')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    
    return render_template('post_d.html', post=post)


@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)






#Допоміжна сторінка 
@main.route('/help')
def helper():
    print(current_user)
    return 'this is help page'




#Не реалізована функція
@main.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)

