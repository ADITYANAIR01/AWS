# === FILE: app/__init__.py ===
from flask import Flask, render_template
from app.config import Config


def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Initialize OAuth
    from app.auth import init_oauth
    init_oauth(app)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.files import files_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    
    # Root route - redirect to login page
    @app.route('/')
    def index():
        return render_template('login.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('login.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return "Internal Server Error", 500
    
    return app
