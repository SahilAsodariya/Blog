from .extensions import db
from datetime import datetime, timedelta

def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships to children with cascade
    posts = db.relationship('Post', backref='user', lazy=True, cascade='all, delete')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_ist_time)
    file = db.Column(db.String(255))

    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_ist_time)

# just for information and reffer

# post.user	The user who wrote the post
# user.posts	All posts written by the user
# post.comments	All comments on the post
# comment.post	The post the comment belongs to
# comment.user	The user who wrote the comment
# user.comments	All comments written by the user