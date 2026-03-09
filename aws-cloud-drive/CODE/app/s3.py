# === FILE: app/s3.py ===
import boto3
from botocore.exceptions import ClientError
from app.config import Config


def get_s3_client():
    """Create and return an S3 client using IAM role credentials."""
    return boto3.client('s3', region_name=Config.AWS_REGION)


def upload_file(file_obj, s3_key, content_type):
    """
    Upload a file to S3.
    
    Args:
        file_obj: File object to upload
        s3_key: S3 key (path) for the file
        content_type: MIME type of the file
    
    Returns:
        True if successful, raises exception otherwise
    """
    try:
        s3_client = get_s3_client()
        
        s3_client.upload_fileobj(
            file_obj,
            Config.S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                'ContentType': content_type
            }
        )
        
        return True
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        raise


def delete_file(s3_key):
    """
    Delete a file from S3.
    
    Args:
        s3_key: S3 key (path) of the file to delete
    
    Returns:
        True if successful, False otherwise
    """
    try:
        s3_client = get_s3_client()
        
        s3_client.delete_object(
            Bucket=Config.S3_BUCKET_NAME,
            Key=s3_key
        )
        
        return True
    except ClientError as e:
        print(f"Error deleting file from S3: {e}")
        return False


def generate_presigned_url(s3_key, expiry=900):
    """
    Generate a presigned URL for downloading a file.
    
    Args:
        s3_key: S3 key (path) of the file
        expiry: Expiration time in seconds (default 15 minutes)
    
    Returns:
        Presigned URL string
    """
    try:
        s3_client = get_s3_client()
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': Config.S3_BUCKET_NAME,
                'Key': s3_key
            },
            ExpiresIn=expiry
        )
        
        return url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise


def generate_share_url(s3_key, expiry=604800):
    """
    Generate a presigned URL for sharing a file (valid for 7 days).
    
    Args:
        s3_key: S3 key (path) of the file
        expiry: Expiration time in seconds (default 7 days)
    
    Returns:
        Presigned URL string
    """
    return generate_presigned_url(s3_key, expiry)


def get_cloudfront_url(s3_key):
    """
    Generate a CloudFront URL for a file (for preview purposes).
    
    Args:
        s3_key: S3 key (path) of the file
    
    Returns:
        CloudFront URL string
    """
    if Config.CLOUDFRONT_DOMAIN:
        return f"https://{Config.CLOUDFRONT_DOMAIN}/{s3_key}"
    else:
        # Fallback to S3 URL if CloudFront is not configured
        return f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}"
