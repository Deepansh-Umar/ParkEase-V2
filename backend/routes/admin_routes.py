# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt,jwt_required
from extensions import db,cache
from models import ParkingLot, ParkingSpot, User, Reservation
import utils,os
from celery_folder.tasks import export_reservations 
from flask import send_file
from celery.result import AsyncResult


admin_bp = Blueprint("admin_bp", __name__)


# ADMIN AUTH MIDDLEWARE

@admin_bp.before_request
def check_admin():
    # Allow OPTIONS
    if request.method == "OPTIONS":
        return None

    # Allow public endpoints for downloading
    open_endpoints = [
        "admin_bp.download_file",
        "admin_bp.task_status"
    ]
    if request.endpoint in open_endpoints:
        return None

    # JWT enforcing
    try:
        jwt_required()(lambda: None)()
    except Exception:
        return jsonify({"error": "Missing or invalid token"}), 401

    # Role check
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403




# Dashboard

@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return jsonify({"message": "Admin Dashboard OK"}), 200



# GET all lots

@admin_bp.route("/lots", methods=["GET"])
@cache.cached(timeout=180, key_prefix="admin_lots")
def get_lots():
    lots = ParkingLot.query.all()
    result = []

    for lot in lots:
        result.append({
            "id": lot.id,
            "name": lot.name,
            "address": lot.address,
            "pincode": lot.pincode,
            "hourly_price": lot.hourly_price,
            "max_spots": lot.max_spots,
            "in_use": lot.in_use
        })

    return jsonify(result), 200



# CREATE new lot

@admin_bp.route("/lots", methods=["POST"])
def add_lot():
    data = request.get_json()

    required = ["name", "address", "pincode", "max_spots", "hourly_price"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing fields"}), 400

    new_lot = ParkingLot(
        name=data["name"],
        address=data["address"],
        pincode=data["pincode"],
        max_spots=int(data["max_spots"]),
        hourly_price=float(data["hourly_price"])
    )

    db.session.add(new_lot)
    db.session.commit()
    cache.delete("admin_lots")
    cache.delete("user_lots")

    utils.init_spots(new_lot.id, new_lot.max_spots)

    return jsonify({"message": "Lot added successfully"}), 201



# UPDATE lot

@admin_bp.route("/lots/<int:lot_id>", methods=["PUT"])
def edit_lot(lot_id):
    data = request.get_json()
    lot = ParkingLot.query.get_or_404(lot_id)

    prev_spots = lot.max_spots

    lot.name = data.get("name", lot.name)
    lot.address = data.get("address", lot.address)
    lot.pincode = data.get("pincode", lot.pincode)
    lot.hourly_price = data.get("hourly_price", lot.hourly_price)

    new_spots = int(data.get("max_spots", lot.max_spots))

    # Adjust spots if changed
    if new_spots != prev_spots:
        err = utils.edit_spots(lot.id, new_spots)
        if err:
            return jsonify({"error": err}), 403
        lot.max_spots = new_spots

    db.session.commit()
    cache.delete("admin_lots")
    cache.delete("user_lots")
    return jsonify({"message": "Lot updated"}), 200



# DELETE lot

@admin_bp.route("/lots/<int:lot_id>", methods=["DELETE"])
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if lot.in_use > 0:
        return jsonify({"error": "Cannot delete — active reservations exist"}), 403

    db.session.delete(lot)
    db.session.commit()
    cache.delete("admin_lots")
    cache.delete("user_lots")
    return jsonify({"message": "Lot deleted"}), 200



# GET all users

@admin_bp.route("/users", methods=["GET"])
@cache.cached(timeout=300, key_prefix="admin_users")
def view_users():
    users = User.query.all()
    result = []

    for u in users:
        if u.role!="admin":
            result.append({
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role
            })

    return jsonify(result), 200



# User summary (admin view)

@admin_bp.route("/summary/<user_id>", methods=["GET"])
def user_summary_by_admin(user_id):
    user = User.query.get_or_404(user_id)

    d = utils.get_user_summary_data(user)

    bookings = []
    for r in d["bookings"]:
        bookings.append({
            "id": r.id,
            "lot": r.lot.name,
            "spot": r.spot_id,
            "start_time": str(r.start_time),
            "leave_time": str(r.leave_time),
            "total_cost": r.total_cost
        })

    return jsonify({
        "user": user.username,
        "bookings": bookings,
        "top_usage": d["top_usage"],
        "fav_spots": d["fav_spots"]
    }), 200



# Lot-wise summary (charts)

@admin_bp.route("/lotwise_summary", methods=["GET"])
def lotwise_summary():
    data = utils.admin_summary_data()
    return jsonify({
        "top_users": data["top_users"],
        "top_lots": data["top_lots"]
    }), 200



# View spots under a lot

@admin_bp.route("/lots/<int:lot_id>/spots", methods=["GET"])
def view_spots(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

    result = []
    for s in spots:
        result.append({
            "id": s.id,
            "lot_id": s.lot_id,
            "status": s.status
        })

    return jsonify(result), 200


@admin_bp.route("/export", methods=["POST"])
def export_admin_data():

    task = export_reservations.delay(user_id=None, is_admin=True)
    return jsonify({"task_id": task.id}), 202



@admin_bp.route("/download/<task_id>", methods=["GET"])
def download_file(task_id):

    folder = "./celery_folder/exported_files"
    for f in os.listdir(folder):
        if task_id in f:
            return send_file(os.path.join(folder, f), as_attachment=True)

    return jsonify({"error": "file not ready"}), 404

@admin_bp.route("/task/<task_id>", methods=["GET"])
def task_status(task_id):
    result = AsyncResult(task_id)
    return jsonify({"status": result.status})
