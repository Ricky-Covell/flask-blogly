
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


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
    return render_template('home.html')



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

@app.route('/posts')
def show_all_posts():
    posts = Post.query.all()
    return render_template('/posts/post-index.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/create-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title = request.form['new-post-title'],
        content = request.form['new-post-content'],
        user_id = user.id,
        tags = tags   
    )

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')
    

@app.route('/posts/<int:post_id>/', methods=['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/show-post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def commit_edited_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['edited-post-title'],
    post.content = request.form['edited-post-content'],

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')






# # # # # # # # # # # # # # TAG ROUTES # # # # # # # # # # # # # # # # 

@app.route('/tags', methods=['GET'])
def show_all_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/tags/tag-index.html', tags=tags)



@app.route('/tags/<int:tag_id>', methods=['GET'])
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show-tag.html', tag=tag)


@app.route('/tags/new', methods=['GET'])
def new_tag_form():
    return render_template('/tags/new-tag.html')


@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    new_tag = Tag(
        name = request.form['tag-name'],
    )
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/edit-tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_edited_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    tag.name = request.form['edited-tag-name']

    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

    

