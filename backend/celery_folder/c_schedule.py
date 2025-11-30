from celery.schedules import crontab
from celery import shared_task
from app import celery_app
from celery_folder.tasks import send_daily_reminders,send_monthly_reports

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(crontab(hour=13, minute=12), send_daily_reminders.s(), name='daily reminder' )

    # sender.add_periodic_task(10.00, send_daily_reminders.s())
    # sender.add_periodic_task(10.00, send_monthly_reports.s())

    sender.add_periodic_task(crontab(hour=13, minute=12, day_of_week='sunday'), send_monthly_reports.s(), name = 'weekly reminder' )

