import os
from flask import Flask

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
BASE_DIR = os.path.dirname(__file__)
DEFAULT_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(DEFAULT_UPLOAD_FOLDER, exist_ok=True)

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-change-me'),
    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', DEFAULT_UPLOAD_FOLDER),
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5 MB
)

# Import routes to register them
from . import routes  # noqa: E402,F401