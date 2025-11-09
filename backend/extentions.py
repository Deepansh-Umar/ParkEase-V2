from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from redis import Redis

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = Redis(host="localhost", port=6379, decode_responses=True)
