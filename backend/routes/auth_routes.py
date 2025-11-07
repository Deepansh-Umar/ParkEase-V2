from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    data = request.get_json()
    return jsonify({"message": f"Login route working!", "data": data}), 200

@auth_bp.route("/signup", methods=["GET","POST"])
def signup():
    data = request.get_json()
    return jsonify({"message": "Signup route working", "data": data}), 201

@auth_bp.route("/logout", methods=["GET","POST"])
def logout():
    return jsonify({"message": "Logout successful"}), 200
