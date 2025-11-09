from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.extentions import db
from models import User
import uuid
from datetime import timedelta

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

#Register route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        user_id=str(uuid.uuid4())[:8],
        username=username,
        email=email,
        password=hashed_password,
        is_admin=False,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


#Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username_or_email = data.get("username_or_email")
    password = data.get("password")

    if not all([username_or_email, password]):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity={"user_id": user.id, "username": user.username, "is_admin": user.is_admin},
        expires_delta=timedelta(hours=6),
    )

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
        },
    }), 200


#Protected route 
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"message": "Welcome to your profile", "user": current_user}), 200
