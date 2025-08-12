from flask import Flask
from .extensions import db, migrate, jwt,mail, socketio
from .routes.auth import auth_bp
from .routes.post import post_bp
from .routes.First_page import bp as first_page_bp
from .routes.comment import comment_bp 
from .routes.admin import admin_bp 

def create_app(config = "config.Config"):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    app.register_blueprint(auth_bp, url_prefix="/auth/")
    app.register_blueprint(post_bp, url_prefix="/post/")
    app.register_blueprint(first_page_bp)
    app.register_blueprint(comment_bp, url_prefix="/comment/")
    app.register_blueprint(admin_bp, url_prefix="/admin/")

    return app