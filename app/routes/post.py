from flask import Blueprint, request, render_template,jsonify, current_app
import os
from werkzeug.utils import secure_filename
from ..models import Post, User
from ..extensions import db
from ..schema.schema import PostSchema, CommentSchema
from datetime import datetime, timedelta
from sqlalchemy import func
from ..utils.image_compres_utils import compress_image



# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

from flask_jwt_extended import jwt_required, get_jwt_identity


post_bp = Blueprint('post', __name__)
post_shcema = PostSchema()
posts_shcema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)


@post_bp.route('/', methods=['GET'])
def get_posts():
    # Get query params with default values
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '', type=str)

    # Paginate query
    
    if search:
        pagination = Post.query.filter(
        func.lower(Post.content).like(f'%{search}%')
        ).order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)
    else:
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=limit)
        
    
    admin = 0
    admin_users = User.query.filter_by(is_admin=True).first()
    if admin_users:
        admin = admin_users.id

    post_list = []
    for post in pagination.items:
        post_list.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "file" : post.file,
            "user_id": post.user_id,
            "username": post.user.username,
            "comments": comments_schema.dump(post.comments) if post.comments else [],
        })
    return jsonify({
        "posts": post_list,
        "admin": admin,
        "pagination": {
            "total_posts": pagination.total,
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }
    }), 200  

@post_bp.route('/create-page', methods=['GET'])
def create_post_page():
    return render_template("create_post.html")

@post_bp.route('/create/', methods=['POST'])
@jwt_required()
def create_post():
    if request.method == 'POST':
        # Default values
        filename = None

        user_id = get_jwt_identity()

        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            file = request.files.get('file')

            # Handle file upload if file is provided and valid
            if file and file.filename != '' and allowed_file(file.filename):
                filename = compress_image(file)

        # Create and save post
        post = Post(title=title, content=content, user_id=user_id, file=filename)
        db.session.add(post)
        db.session.commit()

        return {'message': 'Post created successfully'}, 201

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
    
    filename = None
    if request.method == 'POST' or request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
               
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            file = request.files.get('file')
            
            #Handle file upload if file is provided and valid
            if file and file.filename != '' and allowed_file(file.filename):
                file_name = compress_image(file)
                post.file = file_name
            
            
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
