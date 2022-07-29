import os
from distutils.log import error
from tkinter.tix import DirSelectBox
from flask import render_template, request, redirect, url_for, flash, make_response, session, current_app
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import login_required, login_user, current_user, logout_user
from . import main
from .. import db
from .forms import PostForm, CommentForm
from ..models import Post, Subscribe, User, Comment, Permission, Like , ContactUs, MerchItem
from werkzeug.security import check_password_hash, generate_password_hash




# news subscription handler
@main.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        if len(request.form.get('email')) > 3:
            sub_cl = request.form.get('email')
            param = None

            #a record of those who subscribed to the """file"""
            # with open ('client.txt', 'a', encoding='utf-8') as f:
            #     f.write(f'{sub_cl} \n ' )
            #     flash('You were successfully subscribe !')

            # checking for subscription
            if Subscribe.query.filter(Subscribe.email == f'{sub_cl}').all():
                flash(" You are already subscribed ", category='info')
                param = True
                return render_template('block.html', param=param)

            try:
                # recording in the database
                subscribe_m = Subscribe(email=sub_cl)
                db.session.add(subscribe_m)
                db.session.commit()
                param = True
                flash('You were successfully subscribe !', category='success')
                return render_template('block.html', param=param)

            except BaseException:
                print('db error')
        else:
            flash('Something wrong! Confirm your entries', category ='error')

    return render_template('block.html')




#handler form 'contact_us' at home page
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    email = request.form.get('email')
    name = request.form.get('name')
    subject = request.form.get('subject')
    message = request.form.get('message')
    if email and message :
        new_contactus = ContactUs(name=name,email=email, subject=subject, message= message)
        db.session.add(new_contactus)
        db.session.commit() 
        flash('You were successfully send message !' , category= 'success')
    else:
        flash('Check your entries !' , category= 'error')
    return render_template('block.html')



###writing messages to the """file""" form at home page "contuct_us"
# with open('client.txt', 'a', encoding='utf-8') as f:
#     text = ' '
#     count = 0 
#     for letter in message:
#         text = text+ letter
#         count += 1
#         if letter == ' ' and count > 70:
#             text += '\n'
#             count = 0
#     f.write(f'{name}-{email}-{subject} \n \
#                  {text} \n')
#     flash('You were successfully send message !')



#page with a list of merch items for sale
@main.route('/sales', methods=['GET', 'POST'])
def show_items_sale():
    return render_template('sales/sales.html') 



#add a product for sale to the database
@main.route('/add-item', methods=['GET', 'POST'])
def add_item_merch():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        item =  MerchItem(name=name, description=description, price=price)
        try:    
            db.session.add(item)
            db.session.commit()
            flash('You were successfully add item !' , category= 'success')

        except:    
            flash('Check your entries !' , category= 'error')
    return render_template ('sales/add_item_merch.html')



#view existing products from the database
@main.route('/show-item', methods=['GET'])
@login_required
def show_item():
    #check permission
    if current_user.can(Permission.MODERATE) or current_user.can(Permission.ADMIN):    
        page = request.args.get('page')

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        
        items = MerchItem.query.order_by(MerchItem.created.desc())
        pages = items.paginate(page=page, per_page=5)
        return render_template('sales/list_items.html', items = items, pages=pages)
    return render_template('block.html')



#file extensions that are uploaded to the server are valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in  current_app.config['ALLOWED_EXTENSIONS']


#page for uploading files to the server
@main.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='error')
        file = request.files['file']
      
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', category='error')
            
        if not allowed_file(file.filename) :
            flash('Chose correct file format(permitted jpg)' , category='error')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash( '{"filename" : "%s"}' % filename, category='success' )

    return render_template ('upload.html')
        


#viewing messages from users from the "contact us" form
@main.route('/contact/message', methods=['GET'])
@login_required
def show_contact_msg():
    if current_user.can(Permission.MODERATE) or current_user.can(Permission.ADMIN):
        page = request.args.get('page') 

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        messages = ContactUs.query.order_by(ContactUs.created.desc())
        pages = messages.paginate(page=page, per_page=5)  #create pagination page

        return render_template('messages_contact.html', messages = messages, pages=pages)
    return render_template('block.html')
    


#creating a new blog post
@main.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    if current_user.can(Permission.WRITE):
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            user_id = current_user.id
            try:
                post = Post(title=title, body=body, author_id=user_id)
                db.session.add(post) #add post in db
                db.session.commit()
            except BaseException:
                print('error db.add 498e238e')

            return redirect(url_for('main.index'))

        form = PostForm()
        return render_template('create_post.html', form=form)
    else:    
        flash('No access', category ='error')
    return redirect(url_for('main.index'))



#edit post
@main.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    # check permission
    if current_user.can(Permission.MODERATE):
        post = Post.query.filter(Post.slug == slug).first()

        if request.method == 'POST':
            form = PostForm(formdata=request.form, obj=post)
            form.populate_obj(post)
            db.session.commit()
            return redirect(url_for('main.post_detail', slug=post.slug))

        form = PostForm(obj=post)
        return render_template('edit_post.html', post=post, form=form)
    else:
        flash('No access', category ='error')
    return redirect(url_for('main.index'))



#list titles of posts
@main.route('/blog/posts', methods=['GET', 'POST'])
def index():
    # search only among posts with "search?q="
    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(
            Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)

    return render_template('index.html', posts=posts, pages=pages, page=page)



#removal post by slag
@main.route('/<slug>/delete-post', methods=['POST', 'GET'])
@login_required
def delete_post(slug):
    # check permission
    if current_user.can(Permission.MODERATE) or current_user.can(Permission.ADMIN):
        post = Post.query.filter(Post.slug == slug).first()
        if not post:
            flash("Post does not exist.", category='error')
        
          
        else:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted.', category='success')
    else:
        flash('You do not have permission to delete this post.', category='error')
    
    return redirect (url_for('main.index'))



# delete comment by id
@main.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    slug = Post.query.filter(Post.id == comment.post_id).first().slug

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author_id and current_user.id != comment.post.author_id:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.post_detail', slug=slug))
    return redirect(url_for('main.index'))



# home page 
@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home_view():

    return render_template('block.html')



#detailed information about the post with comments
@main.route('/post/<slug>/', methods=['GET', 'POST'])
def post_detail(slug):
    post_id = Post.query.filter(Post.slug == slug).first().id
    post = Post.query.filter_by(id=post_id).first()
    form = CommentForm()
    page = request.args.get('page', type=int)

    if form.validate_on_submit():
        if post:
            # add comment in database
           
            comment = Comment(
                body=form.body.data, author=current_user._get_current_object(), post=post,)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
            return redirect(url_for('main.index'))
    if page:
        page = int(page)
    else:
        page = 1
    pagination_lim = 3 
    comments = Comment.query.order_by(Comment.timestamp.desc())
    pages = comments.paginate(page=page, per_page=5)
    

    return render_template('post_d.html', post=post, 
                            comments=comments, page=page, pages=pages, form = form, pagination_lim=pagination_lim)    



# like/ulike post      
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


# help page
@main.route('/help')
def helper():
    print(current_user)
    return 'this is help page'


# user id  
@main.route('/user/<int:id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)
