# === FILE: app/auth.py ===
from functools import wraps
from flask import Blueprint, session, redirect, url_for, request, flash
from authlib.integrations.flask_client import OAuth
from app.config import Config
from app import db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# OAuth client will be initialized in __init__.py
oauth = None


def init_oauth(app):
    """Initialize OAuth with the Flask app."""
    global oauth
    oauth = OAuth(app)
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login')
def login():
    """Redirect to Google OAuth login page."""
    redirect_uri = Config.GOOGLE_REDIRECT_URI
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/callback')
def callback():
    """Handle Google OAuth callback."""
    try:
        # Exchange authorization code for access token
        token = oauth.google.authorize_access_token()
        
        # Get user info from Google
        userinfo = token.get('userinfo')
        
        if not userinfo:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('auth.login'))
        
        # Extract user data
        google_id = userinfo.get('sub')
        email = userinfo.get('email')
        name = userinfo.get('name')
        profile_picture = userinfo.get('picture')
        
        # Get or create user in database
        user = db.get_or_create_user(google_id, email, name, profile_picture)
        
        if not user:
            flash('Failed to create user account.', 'error')
            return redirect(url_for('auth.login'))
        
        # Store user in session
        session['user'] = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'profile_picture': user['profile_picture']
        }
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        return redirect(url_for('files.dashboard'))
        
    except Exception as e:
        print(f"Error during OAuth callback: {e}")
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    """Log out the current user."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
