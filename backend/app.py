import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt, cache
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'parking.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # Redis Cache configuration
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_HOST"] = "localhost"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60  

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    @app.route('/')
    def home():
        return jsonify({"message": "Vehicle Parking Backend Running Successfully!"})

    return app



app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
