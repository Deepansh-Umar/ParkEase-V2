from flask import Blueprint, jsonify, request

lot_bp = Blueprint("lot_bp", __name__)

@lot_bp.route("/", methods=["GET"])
def list_lots():
    return jsonify({"message": "List of parking lots"}), 200

@lot_bp.route("/<int:lot_id>", methods=["GET"])
def get_lot(lot_id):
    return jsonify({"message": f"Details for lot {lot_id}"}), 200
