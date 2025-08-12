from flask import request
from .extensions import socketio, online_users

@socketio.on('register_user')
def register_user(data):
    """Register a user after they connect."""
    user_id = data['user_id']
    online_users[user_id] = request.sid
    print(f"✅ User {user_id} connected with sid {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Remove the user from online list on disconnect."""
    sid_to_remove = None
    for uid, sid in online_users.items():
        if sid == request.sid:
            sid_to_remove = uid
            break
    if sid_to_remove:
        del online_users[sid_to_remove]
        print(f"❌ User {sid_to_remove} disconnected")
