# AWS Cloud Drive

A modern, full-stack cloud file storage application — a mini Dropbox clone built with Python Flask and AWS services. Users can sign in with Google, upload files to S3, manage them via a beautiful dark-themed UI, and share files with others.

![AWS Cloud Drive](https://img.shields.io/badge/AWS-Cloud%20Drive-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Features

- **Google OAuth Authentication** — Secure sign-in with Google accounts
- **File Upload & Storage** — Upload files up to 100MB, stored securely on AWS S3
- **File Management** — View, download, delete, and organize your files
- **File Sharing** — Generate shareable links with 7-day expiration
- **File Preview** — Preview images and PDFs directly in browser
- **Modern UI** — Dark theme with smooth animations and responsive design
- **Cloud Infrastructure** — Built on AWS S3, RDS PostgreSQL, and CloudFront

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11** — Core programming language
- **Flask 3.0** — Web framework
- **PostgreSQL (RDS)** — Relational database for metadata
- **AWS S3** — Object storage for files
- **AWS CloudFront** — CDN for fast file delivery
- **Gunicorn** — Production WSGI server

### Frontend
- **HTML5** — Semantic markup
- **Tailwind CSS** — Utility-first CSS framework
- **Vanilla JavaScript** — No frameworks, pure JS

### Authentication
- **Google OAuth 2.0** — Via Authlib

### Python Libraries
- `Flask` — Web framework
- `Authlib` — OAuth client
- `boto3` — AWS SDK for Python
- `psycopg2` — PostgreSQL adapter
- `python-dotenv` — Environment variable management
- `gunicorn` — Production server

---

## 📁 Project Structure

```
aws-cloud-drive/
│
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration loader
│   ├── auth.py               # Google OAuth blueprint
│   ├── files.py              # File management blueprint
│   ├── db.py                 # Database operations
│   ├── s3.py                 # S3 operations
│   │
│   ├── templates/
│   │   ├── base.html         # Base template with navbar
│   │   ├── login.html        # Login page
│   │   └── dashboard.html    # Main dashboard
│   │
│   └── static/
│       ├── css/
│       │   └── style.css     # Custom styles
│       └── js/
│           └── dashboard.js  # Frontend logic
│
├── sql/
│   └── schema.sql            # Database schema
│
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
├── gunicorn.conf.py          # Gunicorn configuration
└── README.md                 # This file
```

---

## 🔧 Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database (AWS RDS recommended)
- AWS account with S3 bucket
- Google Cloud project with OAuth credentials

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/aws-cloud-drive.git
cd aws-cloud-drive
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=production

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://your-domain.com/auth/callback

AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name
CLOUDFRONT_DOMAIN=your-cloudfront-domain.cloudfront.net

DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432
DB_NAME=clouddrive
DB_USER=dbadmin
DB_PASSWORD=your-db-password
```

### 4. Set Up AWS Resources

#### S3 Bucket
1. Create an S3 bucket in your AWS console
2. Note the bucket name for `.env`
3. Configure IAM role with S3 permissions

#### RDS PostgreSQL
1. Create a PostgreSQL instance in RDS
2. Note the endpoint, port, database name, and credentials
3. Ensure security group allows connections from your EC2 instance

#### CloudFront (Optional)
1. Create a CloudFront distribution pointing to your S3 bucket
2. Note the CloudFront domain for `.env`

#### EC2 IAM Role
Attach an IAM role to your EC2 instance with these policies:
- `AmazonS3FullAccess` (or custom S3 policy)
- `AmazonRDSDataFullAccess` (or custom RDS policy)

### 5. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://your-domain.com/auth/callback`
5. Copy Client ID and Client Secret to `.env`

### 6. Initialize Database

The database will be initialized automatically on first run, or manually:

```bash
python -c "from app.db import init_db; init_db()"
```

### 7. Run the Application

#### Development

```bash
python run.py
```

#### Production (with Gunicorn)

```bash
gunicorn -c gunicorn.conf.py run:app
```

---

## 🚀 Deployment on AWS EC2

### 1. Launch EC2 Instance

- **AMI:** Ubuntu 22.04 LTS
- **Instance Type:** t2.micro (free tier) or t2.small
- **Security Group:**
  - Allow SSH (port 22)
  - Allow HTTP (port 80)
  - Allow HTTPS (port 443)
  - Allow Custom TCP (port 5000) for testing

### 2. SSH into Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

### 4. Clone and Set Up Application

```bash
git clone https://github.com/yourusername/aws-cloud-drive.git
cd aws-cloud-drive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure Nginx (Optional)

Create `/etc/nginx/sites-available/clouddrive`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/clouddrive /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Run with Gunicorn

Install and configure Gunicorn:

```bash
pip install gunicorn
```

Create a systemd service `/etc/systemd/system/clouddrive.service`:

```ini
[Unit]
Description=Cloud Drive Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/aws-cloud-drive
Environment="PATH=/home/ubuntu/aws-cloud-drive/venv/bin"
ExecStart=/home/ubuntu/aws-cloud-drive/venv/bin/gunicorn -c gunicorn.conf.py run:app

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start clouddrive
sudo systemctl enable clouddrive
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** — Use `.env.example` as a template
2. **Use IAM roles** — Avoid hardcoding AWS credentials
3. **HTTPS only** — Use SSL certificates (Let's Encrypt)
4. **Secure session cookies** — Already configured in app
5. **File size limits** — 100MB enforced
6. **Input validation** — Filenames sanitized with `secure_filename`
7. **User isolation** — All file operations verify ownership

---

## 📝 API Endpoints

### Authentication
- `GET /auth/login` — Redirect to Google OAuth
- `GET /auth/callback` — Handle OAuth callback
- `GET /auth/logout` — Log out user

### Files
- `GET /files/` — Dashboard (requires login)
- `POST /files/upload` — Upload file (requires login)
- `GET /files/download/<id>` — Download file (requires login)
- `POST /files/delete/<id>` — Delete file (requires login)
- `POST /files/share/<id>` — Generate share link (requires login)
- `GET /files/preview/<id>` — Preview file (requires login)

---

## 🎨 UI Screenshots

### Login Page
Clean, modern login with Google OAuth

### Dashboard
Dark-themed file manager with upload, download, share, and delete actions

---

## 🛠️ Development

### Run in Development Mode

```bash
export FLASK_ENV=development
python run.py
```

### Database Schema

The schema is defined in `sql/schema.sql`:

- **users** — User accounts from Google OAuth
- **files** — File metadata with S3 keys and share tokens

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- Flask for the excellent web framework
- AWS for reliable cloud infrastructure
- Tailwind CSS for beautiful styling
- Google OAuth for secure authentication

---

**Built with ❤️ using Python, Flask, and AWS**
