from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User
from auth import login_user, logout_user, get_current_user

auth_api = Blueprint("auth_api", __name__)


def _bad_request(message: str, status_code: int = 400):
    return jsonify({"ok": False, "error": message}), status_code


@auth_api.post("/auth/register")
@cross_origin()
def register():
    data = request.get_json(silent=True) or {}
    
    required = ["first_name", "last_name", "email", "phone", "password", "address"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return _bad_request(f"Missing fields: {', '.join(missing)}")
    
    # Check if user already exists
    if User.query.filter_by(email=data["email"]).first():
        return _bad_request("Email already registered", 409)
    
    if User.query.filter_by(phone=data["phone"]).first():
        return _bad_request("Phone already registered", 409)
    
    # Create new user
    user = User(
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        email=data["email"].strip().lower(),
        phone=data["phone"].strip(),
        address=data["address"].strip(),
        password_hash=generate_password_hash(data["password"])
    )
    
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    
    return jsonify({
        "ok": True, 
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 201


@auth_api.post("/auth/login")
@cross_origin()
def login():
    data = request.get_json(silent=True) or {}
    
    if not data.get("email") or not data.get("password"):
        return _bad_request("Email and password required")
    
    user = User.query.filter_by(email=data["email"].strip().lower()).first()
    
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return _bad_request("Invalid email or password", 401)
    
    login_user(user)
    
    return jsonify({
        "ok": True,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    })


@auth_api.post("/auth/logout")
@cross_origin()
def logout():
    logout_user()
    return jsonify({"ok": True})


@auth_api.get("/auth/me")
@cross_origin()
def get_current_user_info():
    user = get_current_user()
    if not user:
        return _bad_request("Not authenticated", 401)
    
    return jsonify({
        "ok": True,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    })
