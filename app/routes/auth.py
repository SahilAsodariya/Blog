from flask import Blueprint, request,render_template, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..extensions import db,socketio
from ..validation import is_valid_password
from ..schema.schema import UserSchema
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity, decode_token
from email_validator import validate_email, EmailNotValidError
from ..utils.email_utils import send_email
from datetime import timedelta




auth_bp = Blueprint('auth',__name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
        
        
@auth_bp.route('register/', methods=['GET','POST'])
def register():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
             
        try:
            valid = validate_email(email)  # it will throw if invalid
            valid_email = valid.email
        except EmailNotValidError as e:
            return jsonify({"message": str(e)}), 400
                
        is_valid, message = is_valid_password(password)
        
        if not is_valid:
            return jsonify({"message":message}),400
        
        registered_email = User.query.filter_by(email=email).first()
        if registered_email:
            return {"message": "Email already registered"}, 400
        else:
            hased_password = generate_password_hash(password)
            new_user = User(username=name, email=valid_email, password=hased_password,  profile_pictures='default_profile.png')
            db.session.add(new_user)
            db.session.commit()
            send_email(
                    subject="Welcome to our website",
                    recipients=[valid_email],
                    body=f"Hi {name},\n\nWelcome to our blog! 🎉\nWe’re excited to have you on board...",
                    html=f"""
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Welcome to our <b>blog</b>! 🎉 We’re excited to have you on board.</p>
                    <ul>
                        <li>Discover new articles</li>
                        <li>Share your own thoughts</li>
                        <li>Leave comments and interact with others</li>
                    </ul>
                    <p>👉 To get started, simply log in and explore the latest posts.</p>
                    <p>If you have any questions or feedback, feel free to reply to this email.</p>
                    <p>Happy reading & writing!<br>— The Blog Team</p>
                    """
                )
            return  jsonify({"message" : "Registration successful, please login."}), 200
    return render_template('register.html')


@auth_bp.route('/')
def hero():
    return render_template('login.html')


@auth_bp.route('login/', methods=['GET','POST'])
@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        is_valid, message = is_valid_password(password)
        
        if not is_valid:
            if request.is_json:
                return jsonify({'message': message}), 401
            else:
                return render_template('login.html', message=message)
    
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                "access_token": access_token,
                "user_id": user.id
            }), 200
        else:
            
            return jsonify({"message": "Invalid email or password"}), 401
    return render_template('login.html')

# route: /reset-password-request
@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
        else:
            email = request.form.get('email')
        try:
            valid = validate_email(email)  # it will throw if invalid
            valid_email = valid.email
        except EmailNotValidError as e:
            return jsonify({"message": str(e)}), 400
        
        user = User.query.filter_by(email=valid_email).first()
        
        if user:
            token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=30))
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            send_email(subject=user.email,
                       recipients=[f"{valid_email}"],
                       body='',
                       html=f'''
                            <h3>Reset Your Password</h3>
                            <p>Click the link below to reset your password:</p>
                            <a href="{reset_url}">Reset Password</a>
                            <p><strong>Note:-</strong> This link will expire in 30 minutes.</p>
                        '''
                       )
            return jsonify({'success': 'If this email exists, a reset link has been sent.'}), 200
        return jsonify({"error": "Please add email that you add to register"}), 400
    return render_template('reset_password_request.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']

    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 400

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_password = data.get('password')
        else:
            new_password = request.form.get('password')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': 'Password has been reset successfully'}), 200

    return render_template('reset_password.html', token=token)
