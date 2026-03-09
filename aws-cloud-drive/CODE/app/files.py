# === FILE: app/files.py ===
import os
import uuid
import secrets
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from app.auth import login_required
from app import db, s3


files_bp = Blueprint('files', __name__, url_prefix='/files')


# Maximum file size: 100MB
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB in bytes


def format_file_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_file_category(file_type):
    """Determine file category based on MIME type."""
    if not file_type:
        return 'other'
    
    file_type = file_type.lower()
    
    if file_type.startswith('image/'):
        return 'image'
    elif file_type == 'application/pdf':
        return 'pdf'
    elif file_type.startswith('video/'):
        return 'video'
    elif file_type.startswith('audio/'):
        return 'audio'
    elif file_type in ['application/zip', 'application/x-zip-compressed', 'application/x-rar-compressed', 'application/x-7z-compressed']:
        return 'archive'
    elif file_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                       'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                       'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                       'text/plain', 'text/csv']:
        return 'document'
    else:
        return 'other'


def format_date(dt):
    """Format datetime to readable string."""
    if not dt:
        return ''
    
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except:
            return dt
    
    return dt.strftime('%b %d, %Y')


@files_bp.route('/')
@login_required
def dashboard():
    """Display the main dashboard with user's files."""
    user_id = session['user']['id']
    
    # Get all files for the user
    files = db.get_files_by_user(user_id)
    
    # Enhance file data with formatted information
    for file in files:
        file['size_formatted'] = format_file_size(file['file_size'] or 0)
        file['category'] = get_file_category(file['file_type'])
        file['date_formatted'] = format_date(file['uploaded_at'])
    
    return render_template(
        'dashboard.html',
        user=session['user'],
        files=files
    )


@files_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle file upload."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'message': 'File size exceeds 100MB limit'}), 400
        
        # Get user ID
        user_id = session['user']['id']
        
        # Secure the filename
        original_name = file.filename
        safe_filename = secure_filename(original_name)
        
        # Generate unique S3 key
        unique_id = uuid.uuid4()
        s3_key = f"{user_id}/{unique_id}_{safe_filename}"
        
        # Get content type
        content_type = file.content_type or 'application/octet-stream'
        
        # Upload to S3
        s3.upload_file(file, s3_key, content_type)
        
        # Save metadata to database
        db.add_file(
            user_id=user_id,
            filename=safe_filename,
            original_name=original_name,
            s3_key=s3_key,
            file_size=file_size,
            file_type=content_type
        )
        
        return jsonify({'success': True, 'message': 'File uploaded successfully'}), 200
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'success': False, 'message': 'Failed to upload file'}), 500


@files_bp.route('/download/<int:file_id>')
@login_required
def download(file_id):
    """Generate presigned URL and redirect for file download."""
    try:
        user_id = session['user']['id']
        
        # Get file from database (verifies ownership)
        file = db.get_file(file_id, user_id)
        
        if not file:
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Generate presigned URL (15 minutes)
        presigned_url = s3.generate_presigned_url(file['s3_key'], expiry=900)
        
        # Redirect to presigned URL
        return redirect(presigned_url)
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return jsonify({'success': False, 'message': 'Failed to download file'}), 500


@files_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete(file_id):
    """Delete a file."""
    try:
        user_id = session['user']['id']
        
        # Get file from database (verifies ownership)
        file = db.get_file(file_id, user_id)
        
        if not file:
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Delete from S3
        s3.delete_file(file['s3_key'])
        
        # Delete from database
        db.delete_file(file_id, user_id)
        
        return jsonify({'success': True, 'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'success': False, 'message': 'Failed to delete file'}), 500


@files_bp.route('/share/<int:file_id>', methods=['POST'])
@login_required
def share(file_id):
    """Generate a shareable link for a file."""
    try:
        user_id = session['user']['id']
        
        # Get file from database (verifies ownership)
        file = db.get_file(file_id, user_id)
        
        if not file:
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Generate share token
        share_token = secrets.token_urlsafe(32)
        
        # Save token to database
        db.set_share_token(file_id, user_id, share_token)
        
        # Generate 7-day presigned URL
        share_url = s3.generate_share_url(file['s3_key'], expiry=604800)
        
        return jsonify({
            'success': True,
            'share_url': share_url
        }), 200
        
    except Exception as e:
        print(f"Error sharing file: {e}")
        return jsonify({'success': False, 'message': 'Failed to generate share link'}), 500


@files_bp.route('/preview/<int:file_id>')
@login_required
def preview(file_id):
    """Generate a preview URL for images and PDFs."""
    try:
        user_id = session['user']['id']
        
        # Get file from database (verifies ownership)
        file = db.get_file(file_id, user_id)
        
        if not file:
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Check if file is previewable (image or PDF)
        file_type = file.get('file_type', '').lower()
        
        if file_type.startswith('image/') or file_type == 'application/pdf':
            # Return CloudFront URL for preview
            preview_url = s3.get_cloudfront_url(file['s3_key'])
            return jsonify({'success': True, 'preview_url': preview_url}), 200
        else:
            # Not previewable, redirect to download
            return redirect(url_for('files.download', file_id=file_id))
        
    except Exception as e:
        print(f"Error generating preview: {e}")
        return jsonify({'success': False, 'message': 'Failed to generate preview'}), 500
