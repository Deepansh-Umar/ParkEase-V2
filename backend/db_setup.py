from app import create_app, db
from models import User
import uuid

def setup_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if admin exists
        if not User.query.filter_by(username="admin").first():
            admin = User(
                id=str(uuid.uuid4()),
                username="admin",
                email="admin@gmail.com",
                password="admin@iitm", 
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("ℹ️ Admin user already exists.")

if __name__ == "__main__":
    setup_db()
