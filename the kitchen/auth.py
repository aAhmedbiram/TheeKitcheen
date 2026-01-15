from functools import wraps
from flask import request, jsonify, session
from models import User


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in via session
        if 'user_id' not in session:
            return jsonify({"ok": False, "error": "Authentication required"}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return jsonify({"ok": False, "error": "Invalid session"}), 401
            
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"ok": False, "error": "Authentication required"}), 401
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({"ok": False, "error": "Admin access required"}), 403
            
        return f(*args, **kwargs)
    return decorated_function


def login_user(user):
    """Store user in session"""
    session['user_id'] = user.id
    session['is_admin'] = user.is_admin


def logout_user():
    """Clear user session"""
    session.clear()


def get_current_user():
    """Get current logged in user"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])
