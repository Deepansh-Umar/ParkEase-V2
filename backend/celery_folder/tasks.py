from celery import shared_task
import csv, os
from models import Reservation
from extensions import db
from celery_folder.mails import send_email, daily_reminder_template, monthly_report_template
from models import User
from datetime import datetime

@shared_task(bind=True)
def export_reservations(self, user_id=None, is_admin=False):

    if is_admin:
        rows = Reservation.query.all()
    else:
        rows = Reservation.query.filter_by(user_id=user_id).all()

    folder = "./celery_folder/exported_files"
    os.makedirs(folder, exist_ok=True)

   
    filename = f"reservations_{user_id or 'all'}_{self.request.id}.csv"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "ID", "User", "Lot", "Spot",
            "Start Time", "Leave Time",
            "Total Cost", "Hourly Cost", "Status"
        ])

        for r in rows:
            writer.writerow([
                r.id,
                r.user.username,
                r.lot.name,
                r.spot_id,
                str(r.start_time),
                str(r.leave_time or ""),
                r.total_cost or 0,
                r.hourly_cost,
                r.status
            ])

    return filename




@shared_task(ignore_result=True)
def send_daily_reminders():
    users = User.query.filter(User.role == 'user').all()


    for u in users:
        html = daily_reminder_template(u.username)
        send_email(u.email, "Daily Reminder", html)



@shared_task(ignore_result=True)
def send_monthly_reports():
    users = User.query.filter(User.role == 'user').all()
    
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year

    for u in users:

        reservations = Reservation.query.filter(
            Reservation.user_id == u.id,
            db.extract("month", Reservation.start_time) == now.month,
            db.extract("year", Reservation.start_time) == now.year
        ).all()

        total_cost = sum(r.total_cost or 0 for r in reservations)

        html = monthly_report_template(
            username=u.username,
            reservations=reservations,
            total_cost=total_cost,
            month=month,
            year=year
        )

        send_email(
            u.email,
            f"{month} Parking Report",
            html
        )
