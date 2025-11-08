from app import app
from extenstion import db
from models import User
import uuid
from werkzeug.security import generate_password_hash

def setup_db():
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if admin exists
        if not User.query.filter_by(username="admin").first():
            hashed_pw = generate_password_hash("admin@iitm", method="pbkdf2:sha256", salt_length=16)
            admin = User(
                
                user_id = "iitmadmin",
                username="admin",
                email="admin@gmail.com",
                password=hashed_pw,
                is_admin = True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    setup_db()
