# === FILE: run.py ===
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app
from app.db import init_db

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Initialize database on first run
    # try:
    #     init_db()
    # except Exception as e:
    #     print(f"Database initialization warning: {e}")
    #     print("Make sure database is accessible and schema.sql exists")
    print("Skipping database initialization - configure DB connection first")
    
    # Run the application
    # host 0.0.0.0 makes the app accessible externally
    # port 5000 is the default Flask port
    # debug should be False in production
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
