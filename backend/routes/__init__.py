from .auth_routes import auth_bp
from .user_routes import user_bp
from .admin_routes import admin_bp
from .lot_routes import lot_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(lot_bp, url_prefix="/api/lots")
