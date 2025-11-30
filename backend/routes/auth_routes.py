# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db,cache
from models import User
from utils import generate_user_id

auth_bp = Blueprint("auth_bp", __name__)

#  REGISTER 
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = generate_password_hash(password)

    user = User(
        id=str(generate_user_id()),
        username=username,
        email=email,
        password=hashed_pw,
        role="user"
    )

    db.session.add(user)
    db.session.commit()
    cache.delete("admin_users")

    return jsonify({"message": "Registration successful"}), 201


#  LOGIN 
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # lot of issues with jwt string vs json format
    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": token,
        "role": user.role,
        "user_id": user.id,
        "username": user.username
    }), 200
