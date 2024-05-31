
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shh'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/')
def home():
    '''Redirects to Index of Users'''
    return redirect('/users')



# # # # # # # # # # # # # # USER ROUTES # # # # # # # # # # # # # # # # 

@app.route('/users')
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/user-index.html', users=users) 




@app.route('/users/new', methods=['GET'])
def add_user_form():
    
    return render_template('users/new-user.html')



@app.route('/users/new', methods=['POST'])
def add_user():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        img_url  = request.form['img_url'] or None
    )  
    db.session.add(new_user)
    db.session.commit()   
    return redirect('/users')



@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show-user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_user_changes(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name_edit']
    user.last_name = request.form['last_name_edit']
    user.img_url = request.form['img_url_edit']

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')



# # # # # # # # # # # # # # POST ROUTES # # # # # # # # # # # # # # # # 



@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/create-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['new-post-title'],
        content = request.form['new-post-content'],
        user_id = user.id
    )

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')
    

@app.route('/posts/<int:post_id>/', methods=['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def commit_edited_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['edited-post-title'],
    post.content = request.form['edited-post-content'],

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')