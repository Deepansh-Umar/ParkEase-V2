from extensions import db
from models import User
# from app import app
from werkzeug.security import generate_password_hash


def setup_db(app):
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username="admin").first():
            admin = User(
                id="admins",
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("👑 Admin created")
        else:
            print("ℹ️ Admin already exists")

# if __name__ == "__main__":
#     setup_db()
