from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from ..models import User,Post, Comment

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        
    id = auto_field()
    username = auto_field()
    email = auto_field()
    is_admin = auto_field()
    posts = auto_field()
    comments = auto_field()
    joined_at = auto_field()
    profile_pictures = auto_field()
    
class CommentSchema(SQLAlchemySchema):
    class Meta:
        model = Comment
        load_instance = True
        
    id = auto_field()
    content = auto_field()
    post_id = auto_field()
    user_id = auto_field()
    created_at = auto_field()
    post = auto_field()
    user = fields.Nested(UserSchema)
    
    
class PostSchema(SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True
        
    id = auto_field()
    title = auto_field()
    content = auto_field()
    user_id = auto_field()
    created_at = auto_field()
    user = fields.Nested(UserSchema)
    Comment = fields.Nested(CommentSchema, many=True)