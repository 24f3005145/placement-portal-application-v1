from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(300), nullable=False)
    role = db.Column(db.Enum('admin','hirer','student', name='role_enum'), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    education = db.Column(db.String(300))       #new
    skills = db.Column(db.String(300))          #new
    contact = db.Column(db.String(300))         #new

    #relationship--------------------------------
    applications = db.relationship('applications', backref='students', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class companies(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50), nullable=False, unique=True)
    hr_contact = db.Column(db.String(50))
    website = db.Column(db.String(50))
    about_company = db.Column(db.String(500))
    password_hash = db.Column(db.String(300), nullable=False)
    approval_status = db.Column(db.Enum('pending','approved','rejected', name='approval_status_enum'), default='pending')
    is_blacklisted = db.Column(db.Integer, default=0)

    #relationship--------------------------------
    placement_drives = db.relationship('placement_drives', backref='companies', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def status_of_approval(self):
        return self.approval_status


class placement_drives(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    job_id = db.Column(db.Integer, nullable=False, unique=True) # NEW    -----------solely for search functionality
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    
    required_skills = db.Column(db.String(300))   # NEW
    experience_required = db.Column(db.String(100))   # NEW
    salary_range = db.Column(db.String(100))   # NEW
    
    eligibility_criteria = db.Column(db.String(500), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    
    status = db.Column(db.Enum('pending','approved','rejected','complete', name='placement_drives_status_enum'), default='pending')

    #relationship--------------------------------
    applications = db.relationship('applications', backref='placement_drives', lazy=True)

class applications(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    application_date = db.Column(db.String(50), nullable=False)
    cv_filename = db.Column(db.String(300), nullable=False)
    status = db.Column(db.Enum('applied','shortlisted','selected','rejected', name='applications_status_enum'), default='applied')



# class admin(db.Model):
#     __tablename__ = 'admin'

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100))
#     password_hash = db.Column(db.String(100))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
