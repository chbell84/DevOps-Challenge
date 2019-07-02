from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = 'app/static/uploads'
UPLOAD_FOLDER_SF = 'static/files'
UPLOAD_FOLDER = 'app/static/files'
API_KEY = 'pUZbiXpKgv1kqXkFMrWQdcqkAgzBpWAC2HAoHNW9EdAIHS7mEHOZixjFapME'
#DEFAULT_FILE = 'app/static/default.csv'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER_SF'] = UPLOAD_FOLDER_SF
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['API_KEY'] = API_KEY
#app.config['DEFAULT_FILE'] = DEFAULT_FILE
#app.config['OUTPUT_FOLDER'] = UPLOAD_FOLDER

from app import routes
