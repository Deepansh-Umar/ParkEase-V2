from models import User, ParkingLot, ParkingSpot, Reservation
from extensions import db,cache
from sqlalchemy import func
from datetime import datetime
import time


# ID GENERATOR

def generate_user_id():
    return int(time.time())



# SPOT INITIALIZATION

def init_spots(lot_id, max_spots):
    for i in range(max_spots):
        spot = ParkingSpot(
            id=f"{lot_id}s{i+1}",
            lot_id=lot_id,
            number=i + 1,
            status="A"
        )
        db.session.add(spot)
    db.session.commit()



# SPOT EDITING (only if no active reservations)

def edit_spots(lot_id, new_count):
    active = (
        db.session.query(ParkingSpot)
        .filter(ParkingSpot.lot_id == lot_id, ParkingSpot.status == "O")
        .count()
    )

    if active > 0:
        return "Cannot update spot count — active reservations exist"

    old_spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    for s in old_spots:
        db.session.delete(s)

    for i in range(new_count):
        spot = ParkingSpot(
            id=f"{lot_id}s{i+1}",
            lot_id=lot_id,
            number=i + 1,
            status="A"
        )
        db.session.add(spot)

    db.session.commit()
    return None



# USER: Active Reservation

def get_user_active_reservations(user_id):
    reservations = Reservation.query.filter_by(
        user_id=user_id,
        status="Active",
        leave_time=None
    ).all()

    if not reservations:
        return []

    return [
        {
            "spot_id": r.spot_id,
            "lot_name": r.lot.name,
            "start_time":  r.start_time.strftime("%d/%m/%Y %H:%M:%S")

        }
        for r in reservations
    ]



# USER: History (Closed reservations)

def get_user_history(user_id):
    records = Reservation.query.filter(
        Reservation.user_id == user_id,
        Reservation.status.in_(["Completed", "Closed"])
    ).all()
    data = []

    for r in records:
        duration_hours = None
        if r.leave_time and r.start_time:
            duration_hours = round((r.leave_time - r.start_time).total_seconds() / 3600, 2)

        data.append({
            "id": r.id,
            "lot_name": r.lot.name,
            "spot_id": r.spot_id,
            "cost": r.total_cost,
            "duration_hours": duration_hours,
            "start": r.start_time.strftime("%d/%m/%Y %H:%M:%S"),
            "end": r.leave_time.strftime("%d/%m/%Y %H:%M:%S") if r.leave_time else None
        })

    return data




# USER: Summary (date → total cost)

@cache.memoize(timeout=180)
def get_user_summary(user_id):
    rows = db.session.query(
        func.date(Reservation.start_time),
        func.sum(Reservation.total_cost)
    ).filter(
        Reservation.user_id == user_id,
        Reservation.status.in_(["Completed", "Closed"])
    ).group_by(func.date(Reservation.start_time)).all()

    return [
        {"date": str(d), "total_cost": float(c or 0)}
        for d, c in rows
    ]



# ADMIN: Summary for ONE user

def get_user_summary_data(user):
    # All bookings
    bookings = Reservation.query.filter_by(user_id=user.id).all()

    # Count per lot
    lot_count = (
        db.session.query(ParkingLot.name, func.count(Reservation.id))
        .join(ParkingSpot, ParkingSpot.lot_id == ParkingLot.id)
        .join(Reservation, Reservation.spot_id == ParkingSpot.id)
        .filter(Reservation.user_id == user.id)
        .group_by(ParkingLot.id)
        .all()
    )

    fav_spots = [{"lot": name, "count": c} for name, c in lot_count]

    return {
        "bookings": bookings,
        "top_usage": len(bookings),
        "fav_spots": fav_spots
    }



# ADMIN: Global Summary (Top users + Top lots)

def admin_summary_data():
    # Top Users
    users = (
        db.session.query(User.username, func.count(Reservation.id))
        .join(Reservation)
        .group_by(User.id)
        .order_by(func.count(Reservation.id).desc())
        .limit(5)
        .all()
    )

    top_users = [{"username": u, "count": int(c)} for u, c in users]

    # Top Lots
    lots = (
        db.session.query(ParkingLot.name, func.count(Reservation.id))
        .join(ParkingSpot, ParkingSpot.lot_id == ParkingLot.id)
        .join(Reservation, Reservation.spot_id == ParkingSpot.id)
        .group_by(ParkingLot.id)
        .limit(5)
        .all()
    )

    top_lots = [{"name": n, "count": int(c)} for n, c in lots]

    return {"top_users": top_users, "top_lots": top_lots}



# ADMIN: Chart Data

def admin_chart_data():
    rows = db.session.query(
        func.date(Reservation.start_time),
        func.count(Reservation.id),
        func.sum(Reservation.total_cost)
    ).group_by(func.date(Reservation.start_time)).all()

    labels, reservations, revenue = [], [], []
    for d, cnt, rev in rows:
        labels.append(str(d))
        reservations.append(cnt)
        revenue.append(float(rev or 0))

    return {
        "labels": labels,
        "reservations": reservations,
        "revenue": revenue
    }

def format_dt(dt):
    return dt.strftime("%d/%m/%Y %H:%M:%S")