from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False, unique = True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    reservations = db.relationship("Reservation", back_populates="user", cascade="all, delete-orphan")



class ParkingLot(db.Model):
    __tablename__ = "parking_lot"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    hourly_price = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    in_use = db.Column(db.Integer, nullable=False, default=0)

    reservations = db.relationship("Reservation", back_populates="lot", cascade="all, delete-orphan")
    spots = db.relationship("ParkingSpot", back_populates="lot", cascade="all, delete-orphan")


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)
    spot_id = db.Column(db.String, db.ForeignKey("parking_spot.id"), nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    leave_time = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    hourly_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="reservations")
    lot = db.relationship("ParkingLot", back_populates="reservations")
    spot = db.relationship("ParkingSpot", back_populates="reservations")


class ParkingSpot(db.Model):
    __tablename__ = "parking_spot"

    id = db.Column(db.String, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    lot = db.relationship("ParkingLot", back_populates="spots")
    reservations = db.relationship("Reservation", back_populates="spot", cascade="all, delete")

