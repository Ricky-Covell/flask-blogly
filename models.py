"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    '''Connects database to Flask'''

    db.app = app
    db.init_app(app)


def drop_db():
    db.drop_database('postgresql:///blogly')

def create_db():
    db.create_database('postgresql:///blogly')    


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"



# # # # # # # # # # # # # # # # # # # DATABASE CLASSES # # # # # # # # # # # # # # # # # # # # # # # # 

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship(
        'Post', 
        backref = 'users', 
        cascade = "all, delete-orphan")



class Post(db.Model):
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, nullable=False, default= datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# Association Table
class PostTag(db.Model):
    
    __tablename__ = 'post_tags'

    id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
     

class Tag(db.Model):
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post', 
        secondary='post_tags', 
        backref = 'tags'
        )    
    





