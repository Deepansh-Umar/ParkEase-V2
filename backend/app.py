import os
from flask import Flask, app
from flask_cors import CORS
from extensions import db, jwt, cache
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from celery_folder.celery_factory import celery_init_app
from celery_folder.tasks import export_reservations


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

    #celery config
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone="Asia/Kolkata"
    ),
)
    celery_init_app(app)
     

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    @app.route('/celery')
    @cache.cached(timeout=3)
    def home():
        task = export_reservations.delay()
        return {"message": task.id}
    

    return app


app = create_app()
celery_app = app.extensions["celery"]
import celery_folder.c_schedule 

if __name__ == '__main__':
    app.run(debug=True)
