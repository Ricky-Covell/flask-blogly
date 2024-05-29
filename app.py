"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


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




@app.route('/users')
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-index.html', users=users) 




@app.route('/users/new', methods=['GET'])
def add_user_form():
    
    return render_template('new-user.html')



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
    return render_template('show-user.html', user=user)



@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_user_changes(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name_edit']
    user.last_name = request.form['last_name_edit']
    user.img_url = request.form['img_url_edit']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')