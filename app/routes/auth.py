from flask import Blueprint, request,render_template, redirect,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..extensions import db
from ..validation import is_valid_password
from ..schema.schema import UserSchema
from flask_jwt_extended import create_access_token,jwt_required


auth_bp = Blueprint('auth',__name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth_bp.route('/')
def hero():
    return render_template('login.html')

@auth_bp.route('login/', methods=['GET','POST'])
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
            return render_template('login.html', message=message)
    
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            return  {"access_token" : access_token , "user_id":user.id}
        else:
            return {"message": "Invalid email or password"}, 401
    return render_template('login.html')
        
        
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
             
        
        is_valid, message = is_valid_password(password)
        
        if not is_valid:
            return render_template('register.html', message=message)
        
        registered_email = User.query.filter_by(email=email).first()
        if registered_email:
            return {"message": "Email already registered"}, 400
        else:
            hased_password = generate_password_hash(password)
            new_user = User(username=name, email=email, password=hased_password)
            db.session.add(new_user)
            db.session.commit()
            return  {"message" : "Registration successful, please login."}
    return render_template('register.html')
            
