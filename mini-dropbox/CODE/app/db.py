# === FILE: app/db.py ===
import psycopg
from psycopg.rows import dict_row
from app.config import Config


def get_connection():
    """Create and return a PostgreSQL database connection."""
    conn = psycopg.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    return conn


def init_db():
    """Initialize the database by creating tables from schema.sql."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Read and execute schema.sql
        with open('sql/schema.sql', 'r') as f:
            schema = f.read()
            cursor.execute(schema)
        
        conn.commit()
        cursor.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_user_by_google_id(google_id):
    """Fetch user by Google ID."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            "SELECT * FROM users WHERE google_id = %s",
            (google_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn:
            conn.close()


def create_user(google_id, email, name, profile_picture):
    """Create a new user and return user dict."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            """
            INSERT INTO users (google_id, email, name, profile_picture)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (google_id, email, name, profile_picture)
        )
        
        user = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Error creating user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_or_create_user(google_id, email, name, profile_picture):
    """Get existing user or create new one (upsert logic)."""
    user = get_user_by_google_id(google_id)
    
    if user:
        return user
    else:
        return create_user(google_id, email, name, profile_picture)


def get_files_by_user(user_id):
    """Get all files for a user, ordered by upload date (newest first)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            """
            SELECT * FROM files
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            """,
            (user_id,)
        )
        
        files = cursor.fetchall()
        cursor.close()
        
        return [dict(f) for f in files] if files else []
    except Exception as e:
        print(f"Error fetching files: {e}")
        return []
    finally:
        if conn:
            conn.close()


def add_file(user_id, filename, original_name, s3_key, file_size, file_type):
    """Add a new file record to the database."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            """
            INSERT INTO files (user_id, filename, original_name, s3_key, file_size, file_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (user_id, filename, original_name, s3_key, file_size, file_type)
        )
        
        file = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        return dict(file) if file else None
    except Exception as e:
        print(f"Error adding file: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def delete_file(file_id, user_id):
    """Delete a file record (with ownership verification)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM files WHERE id = %s AND user_id = %s",
            (file_id, user_id)
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        cursor.close()
        
        return deleted_count > 0
    except Exception as e:
        print(f"Error deleting file: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def get_file(file_id, user_id):
    """Get a single file by ID (with ownership verification)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            "SELECT * FROM files WHERE id = %s AND user_id = %s",
            (file_id, user_id)
        )
        
        file = cursor.fetchone()
        cursor.close()
        
        return dict(file) if file else None
    except Exception as e:
        print(f"Error fetching file: {e}")
        return None
    finally:
        if conn:
            conn.close()


def set_share_token(file_id, user_id, token):
    """Set a share token for a file (with ownership verification)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE files
            SET share_token = %s
            WHERE id = %s AND user_id = %s
            """,
            (token, file_id, user_id)
        )
        
        updated_count = cursor.rowcount
        conn.commit()
        cursor.close()
        
        return updated_count > 0
    except Exception as e:
        print(f"Error setting share token: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def get_file_by_share_token(token):
    """Get a file by its share token (no user_id check for public access)."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(row_factory=dict_row)
        
        cursor.execute(
            "SELECT * FROM files WHERE share_token = %s",
            (token,)
        )
        
        file = cursor.fetchone()
        cursor.close()
        
        return dict(file) if file else None
    except Exception as e:
        print(f"Error fetching file by share token: {e}")
        return None
    finally:
        if conn:
            conn.close()
