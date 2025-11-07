from flask import Blueprint, jsonify

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/dashboard", methods=["GET"])
def user_dashboard():
    return jsonify({"message": "User dashboard API working"}), 200

@user_bp.route("/reservations", methods=["GET"])
def user_reservations():
    return jsonify({"message": "User reservations fetched"}), 200
