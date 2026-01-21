import os
from extensions import db
from models import User
# from app import app
from werkzeug.security import generate_password_hash


def setup_db(app):
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username=os.environ.get("ADMIN_USERNAME")).first():
            admin = User(
                id="admins",
                username=os.environ.get("ADMIN_USERNAME"),
                email=os.environ.get("ADMIN_EMAIL"),
                password=generate_password_hash(os.environ.get("ADMIN_PASSWORD")),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("👑 Admin created")
        else:
            print("ℹ️ Admin already exists")

# if __name__ == "__main__":
#     setup_db()
