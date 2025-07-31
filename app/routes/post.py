from flask import Blueprint, request, render_template,jsonify
from ..models import Post, User
from ..extensions import db
from ..schema.schema import PostSchema, CommentSchema
from datetime import datetime, timedelta

def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

from flask_jwt_extended import jwt_required, get_jwt_identity


post_bp = Blueprint('post', __name__)
post_shcema = PostSchema()
posts_shcema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)


@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    admin = 0
    admin_users = User.query.filter_by(is_admin=True).first()
    if admin_users:
        admin = admin_users.id

    post_list = []
    for post in posts:
        post_list.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "user_id": post.user_id,
            "username": post.user.username,
            "comments": comments_schema.dump(post.comments) if post.comments else [],
        })
    return jsonify({"posts": post_list, "admin": admin}), 200  

@post_bp.route('/create-page', methods=['GET'])
def create_post_page():
    return render_template("create_post.html")

@post_bp.route('/create/', methods=['POST'])
@jwt_required()
def create_post():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user_id = get_jwt_identity()
            title = data.get('title')
            content = data.get('content')
        else:
            user_id = get_jwt_identity()
            title = request.form.get('title')
            content = request.form.get('content')
            
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return {'massage' : 'Post create successfully'}, 201
    return render_template('create_post.html')


@post_bp.route('edit-page/<int:post_id>', methods=['GET'])
def edit_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)
     

@post_bp.route('/update/<int:post_id>',methods=['GET','POST','PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify('Post is not available'), 404
    
    if request.method == 'POST' or request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
               
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            
            
        post.title = title
        post.content = content
        post.created_at = get_ist_time()
        db.session.commit()
        return jsonify('Post updated successfully'), 200
    return render_template('edit_post.html', post=post)

@post_bp.route('/delete/<int:post_id>', methods=['GET','POST','DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify("Post is not available.")
    
    db.session.delete(post)
    db.session.commit()
    return  jsonify({"message":'Post deleted successfully'}), 200
