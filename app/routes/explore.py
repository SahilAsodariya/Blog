from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Post, Subscription
from ..schema.schema import SubscriptionSchema, UserSchema, CommentSchema


explore_bp = Blueprint('explore', __name__)
user_schema = UserSchema()
subscription_schema = SubscriptionSchema()
comments_schema = CommentSchema(many=True)


@explore_bp.route('/explore-page', methods=['GET'])
def explore_page():
    return render_template('explore.html')

@explore_bp.route('/search-users', methods=['GET', 'POST'])
@jwt_required()
def search_users():
    id = get_jwt_identity()
    search = request.args.get('search', '', type=str)
    users = User.query.filter(User.username.like(f"%{search}%"),User.id != id).all() if search else []

    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_pictures": user.profile_pictures
        })
    return {"users": user_list}, 200   

@explore_bp.route('/proifile/<int:user_id>', methods=['GET'])
def view_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    is_admin = user.is_admin if user else False
    user_posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    sub = (
    Subscription.query.filter_by(user_id=user_id)
    .order_by(Subscription.start_date.desc())
    .first())
    is_premium = sub is not None and sub.status == "active"
    
    
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
            "comments": post.comments if post.comments else [],
            
        })

    return (
    render_template(
        "user_profile.html",
        user_data=user_data,
        user=user,
        is_premium=is_premium,
        is_admin=is_admin
    ),
    200,
)

     
