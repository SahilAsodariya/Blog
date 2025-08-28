from flask import Blueprint, render_template, jsonify, request
from ..models import User, Post, Subscription
from ..schema.schema import CommentSchema,UserSchema,SubscriptionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.image_compres_utils import compress_image
from ..extensions import db


profile_bp = Blueprint('profile', __name__)

user_schema = UserSchema()
comments_schema = CommentSchema(many=True)
subscription_schema = SubscriptionSchema()

@profile_bp.route('/')
def profile_page():
    return render_template('profile.html')


@profile_bp.route('/data/<int:id>')
@jwt_required()
def profile_data(id):
    user = User.query.filter_by(id=id).first()
    admin = user.is_admin if user else False
    user_posts = Post.query.filter_by(user_id=id).order_by(Post.created_at.desc()).all()
    sub = (
    Subscription.query.filter_by(user_id=id)
    .order_by(Subscription.start_date.desc())
    .first())
    is_premium = sub is not None and sub.status == "active"

    subscription_end_date = subscription_schema.dump(user.subscription)['end_date'] if is_premium else None
    
    
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

    return jsonify({'user_data' : user_data, "user" : user_schema.dump(user), "is_premium" : is_premium, "subscription_end_date" : subscription_end_date if is_premium else None, "admin" : admin}), 200
    
    
@profile_bp.route('/add_profile_pic/<int:id>')
def profile_pic(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    profile_pic = user.profile_pictures
    return render_template('add_profile_pic.html', profile_pic=profile_pic, user_id=id)

@profile_bp.route('/edit_profile_pic', methods=['POST'])
@jwt_required()
def edit_profile_pic():
    if request.method == 'POST':
        id = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        picture = request.files.get('profile_pictures')
        
        if picture:
            fileName = compress_image(picture,id)
            user.profile_pictures = fileName
            db.session.commit()
            return jsonify({"message": "Profile picture updated successfully"}), 200
        
        return jsonify({"message": "No picture provided"}), 400
        
