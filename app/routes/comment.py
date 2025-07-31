from flask import Blueprint, request, render_template,jsonify
from ..models import Comment
from ..extensions import db
from ..schema.schema import CommentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


comment_bp = Blueprint('comment', __name__)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comment_bp.route('/add_comment/<int:post_id>', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            content = data.get('content')
            
        else:
            content = request.form.get('content')
            
        user_id = get_jwt_identity()
        comment = Comment(content=content, post_id=post_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
    
        return jsonify({"message": "Comment added successfully"}), 201
    return jsonify({"message": "Invalid request"}), 400 

        

