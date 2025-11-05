from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from redis import Redis

from config import Config
from routes import register_routes 

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = Redis(host="localhost", port=6379, decode_responses=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    
    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
