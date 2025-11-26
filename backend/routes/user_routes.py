from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import ParkingLot, ParkingSpot, Reservation, User
from datetime import datetime
from extensions import cache
from utils import get_user_history, get_user_summary, get_user_active_reservations,format_dt

user_bp = Blueprint('user', __name__)

# ---------------------------------------
# 1. Allow OPTIONS before checking JWT
# ---------------------------------------
@user_bp.before_request
def allow_options():
    if request.method == "OPTIONS":
        return None

# ---------------------------------------
# 2. JWT + role check
# ---------------------------------------
@user_bp.before_request
def user_only():
    # Skip OPTIONS safely
    if request.method == "OPTIONS":
        return None

    # Verify JWT here
    try:
        jwt_required()(lambda: None)()
    except Exception:
        return jsonify({"error": "Missing or invalid token"}), 401

    # Check role
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "Users only"}), 403


# ---------------- LOTS ----------------
@cache.cached(timeout=240)
@user_bp.route('/lots', methods=['GET'])
def view_lots():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        data.append({
            "id": lot.id,
            "name": lot.name,
            "address": lot.address,
            "pincode": lot.pincode,
            "available_spots": available,
            "hourly_price": lot.hourly_price
        })
    return jsonify(data), 200


# ---------------- RESERVE ----------------
@user_bp.route('/reserve/<int:lot_id>', methods=['POST'])
def reserve_spot(lot_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    lot = ParkingLot.query.get(lot_id)
    if lot.in_use < lot.max_spots:
        lot.in_use += 1
    if not spot:
        return jsonify({"error": "No available spots"}), 400

    spot.status = 'O'
    reservation = Reservation(
        user_id=user.id,
        lot_id=lot_id,
        spot_id=spot.id,
        start_time=datetime.utcnow(),
        hourly_cost=spot.lot.hourly_price,
        status="Active"
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": f"Spot {spot.id} reserved",
        "spot_id": spot.id
    }), 200


# ---------------- VACATE ----------------
@user_bp.route('/release/<string:spot_id>', methods=['POST'])
def release_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot or spot.status != 'O':
        return jsonify({"error": "Invalid spot or not occupied"}), 400

    reservation = Reservation.query.filter_by(
        spot_id=spot_id,
        status="Active"
    ).first()

    if not reservation:
        return jsonify({"error": "No active reservation found"}), 400

    # ---- Update status ----
    spot.status = "A"

    reservation.leave_time = datetime.utcnow()
    reservation.status = "Completed"
    lot = ParkingLot.query.get(spot.lot_id)
    if lot.in_use > 0:
        lot.in_use -= 1

    duration_hours = (reservation.leave_time - reservation.start_time).total_seconds() / 3600
    cost = round(duration_hours * reservation.hourly_cost, 2)

    reservation.total_cost = cost

    db.session.commit()

    return jsonify({
        "message": f"Spot {spot.id} released successfully",
        "cost": cost,
        "time_hours": round(duration_hours, 2),
        "start": format_dt(reservation.start_time),
        "end": format_dt(reservation.leave_time)
    }), 200




# ---------------- ACTIVE RESERVATIONS ----------------
@user_bp.route('/active', methods=['GET'])
def user_active():
    user_id = get_jwt_identity()
    return jsonify(get_user_active_reservations(user_id)), 200



# ---------------- SUMMARY ----------------
@user_bp.route('/summary', methods=['GET'])
def summary():
    user_id = get_jwt_identity()

    return jsonify({
        "summary": get_user_summary(user_id),
        "history": get_user_history(user_id)
    }), 200
