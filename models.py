from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Enum('admin','company','student', name='role_enum'), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.String(50), nullable=False)

    #relationship--------------------------------
    applications = db.relationship('applications', backref='students', lazy=True)

class companies(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50), nullable=False)
    hr_contact = db.Column(db.String(50))
    website = db.Column(db.String(50))
    approval_status = db.Column(db.Enum('pending','approved','rejected', name='approval_status_enum'), default='pending')
    is_blacklisted = db.Column(db.Integer, default=0)

    #relationship--------------------------------
    placement_drives = db.relationship('placement_drives', backref='companies', lazy=True)

class placement_drives(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    eligibility_criteria = db.Column(db.String(500), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('pending','approved','closed', name='placement_drives_status_enum'), default='pending')
    created_at = db.Column(db.String(50), nullable=False)

    #relationship--------------------------------
    applications = db.relationship('applications', backref='placement_drives', lazy=True)

class applications(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    application_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('applied','shortlisted','selected','rejected', name='applications_status_enum'), default='applied')


