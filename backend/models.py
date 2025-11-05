from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # custom user id
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship("Reservation", back_populates="user")

class ParkingLot(db.Model):
    __tablename__ = "parking_lots"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship("ParkingSpot", back_populates="lot")

class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"))

    lot = db.relationship("ParkingLot", back_populates="spots")
    reservations = db.relationship("Reservation", back_populates="spot")

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spots.id"))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="active")

    user = db.relationship("User", back_populates="reservations")
    spot = db.relationship("ParkingSpot", back_populates="reservations")

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id"))
    amount = db.Column(db.Float, nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)
