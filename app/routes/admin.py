from flask import jsonify,Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request,jwt_required
from functools import wraps
from ..extensions import db
from ..models import User,Post
from ..schema.schema import UserSchema# update with actual import

admin_bp = Blueprint('admin',__name__)

users_shcema = UserSchema(many=True)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # ensures token is valid
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required!!"}), 403

        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/only_admin')
def only_admin():
    return render_template("admin_dashboard.html")

@admin_bp.route('/users', methods=['GET'])
@admin_required
@jwt_required()
def all_users():
    users = User.query.filter_by(is_admin=False).all()
    return jsonify(users_shcema.dump(users)), 200
    
@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE', 'POST','GET'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return render_template("admin_dashboard.html", message="User deleted successfully")
    return jsonify({"error": "User not found"}), 404

    
