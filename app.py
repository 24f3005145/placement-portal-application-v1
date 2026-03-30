from flask import Flask, render_template
from models import db
import os

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#cv File Save System
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#===================================================================================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/placed')
def placed():
    return "Congratulations you have been placed !! HR will contact you soon."
#===================================================================================================================

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)