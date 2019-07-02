from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER_SF = 'static/files'
UPLOAD_FOLDER = 'app/static/files'
API_KEY = 'pUZbiXpKgv1kqXkFMrWQdcqkAgzBpWAC2HAoHNW9EdAIHS7mEHOZixjFapME'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER_SF'] = UPLOAD_FOLDER_SF
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['API_KEY'] = API_KEY

from app import routes
