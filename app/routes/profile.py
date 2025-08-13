from flask import Blueprint, render_template, jsonify
from ..models import User, Post
from ..schema.schema import CommentSchema,UserSchema
from flask_jwt_extended import jwt_required


profile_bp = Blueprint('profile', __name__)

user_schema = UserSchema()
comments_schema = CommentSchema(many=True)

@profile_bp.route('/')

def profile_page():
    return render_template('profile.html')

@profile_bp.route('/data/<int:id>')
@jwt_required()
def profile_data(id):
    user = User.query.filter_by(id=id).first()
    user_posts = Post.query.filter_by(user_id=id).order_by(Post.created_at.desc()).all()
    
    user_data = []
    for post in user_posts:
        user_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "file" : post.file,
            "user_id": post.user_id,
            "username": post.user.username,
            "email" : post.user.email,
            "total_post" : len(user_posts),
            "comments": comments_schema.dump(post.comments) if post.comments else [],
            
        })

    return jsonify({'user_data' : user_data, "user" : user_schema.dump(user)}), 200
    
    