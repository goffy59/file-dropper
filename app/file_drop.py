from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageDraw
from functools import lru_cache
import os
import time
import random

# Logging setup
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Automatically generate a secret key using os.urandom if not set
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # Generate a 24-byte random key if not set in the environment

# Load config from environment variables or defaults
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('FLASK_MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default, change via env

# Log after configuration
app.logger.debug(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize Basic Auth
auth = HTTPBasicAuth()

# Load username and password hash from environment or fallback to default
AUTH_USERNAME = os.getenv("FILEDROPPER_USERNAME", "user")
AUTH_PASSWORD = os.getenv("FILEDROPPER_PASSWORD", "password")
hashed_password = generate_password_hash(AUTH_PASSWORD)

@auth.verify_password
def verify_password(username, password):
    if username == AUTH_USERNAME and check_password_hash(hashed_password, password):
        return True
    return False

# Enable the middleware to handle proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app)

# Function to generate a random favicon (dragon-like design)
def generate_favicon():
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    # Create a blank square image (64x64 pixels for favicon)
    img = Image.new('RGBA', (64, 64), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Randomly create a "dragon-like" design
    for _ in range(random.randint(3, 6)):
        x1 = random.randint(10, 50)
        y1 = random.randint(10, 50)
        x2 = random.randint(x1 + 10, 60)
        y2 = random.randint(y1 + 10, 60)
        draw.ellipse([x1, y1, x2, y2], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Add a random "eye"
    eye_x = random.randint(20, 50)
    eye_y = random.randint(20, 50)
    draw.ellipse([eye_x, eye_y, eye_x + 10, eye_y + 10], fill=(0, 0, 0))

    # Save the image as favicon.ico
    img.save('static/favicon.ico')

# Call favicon generation
generate_favicon()

# Serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('index'))

        if not allowed_file(file.filename):
            flash('Invalid file type!', 'error')
            return redirect(url_for('index'))

        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File uploaded successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('index'))

        return redirect(url_for('index'))  # No need for sleep delay here

    filenames = get_uploaded_files()
    return render_template('index.html', filenames=filenames)

@app.route('/download/<filename>', methods=['GET'])
@auth.login_required  # Protect this route with authentication
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        flash('File not found or inaccessible.', 'error')
        return redirect(url_for('index'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'tar', 'gz', 'bz2', 'tar.gz', 'tar.bz2', 'rar', 
        '7z', 'exe', 'msi', 'csv', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'mp3', 'mp4', 'avi', 'mkv',
        'html', 'json', 'xml', 'apk', 'iso', 'tgz', 'deb', 'rpm', 'rom', 'sh'
    }
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_uploaded_files():
    try:
        return os.listdir(app.config['UPLOAD_FOLDER'])
    except Exception as e:
        flash(f'Error accessing uploaded files: {str(e)}', 'error')
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
