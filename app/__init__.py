from flask import Flask,redirect,render_template,request,session,send_from_directory,send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FASISME123'
UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

from app.models import *
from app.import_excel import get_excel
from app.send_ import send_notif
from app.routes import *


