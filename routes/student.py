from flask import Blueprint, render_template, request, redirect, session, url_for, send_from_directory, current_app
from models import students, companies, placement_drives, applications, db
from datetime import date
from werkzeug.utils import secure_filename
import os

student_bp = Blueprint('student', __name__)

#Student routes========================================================================================================    
@student_bp.route('/student/dashboard', methods=['GET','POST'])
def student_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('auth.Login'))

    company_list = companies.query.all()
    student = students.query.filter_by(id=session['user_id']).first()
    
    return render_template('student/student_dashboard.html',
    name=student.name,
    company_list=company_list,
    drive_applications=student.applications,
    student_id=student.id)
    
#==================================================================================================================
@student_bp.route('/student/application_history', methods=['GET','POST'])
def student_application_history():
    if not session.get('user_id'):
        return redirect(url_for('auth.Login'))

    student = students.query.filter_by(id=session['user_id']).first()
    
    return render_template('student/student_application_history.html',
    id=student.id,
    name=student.name,
    email=student.email,
    department=student.department,
    education=student.education,
    skills=student.skills,
    contact=student.contact,
    applications=student.applications)

#==================================================================================================================
@student_bp.route('/student/view_cv/<filename>')
def view_cv(filename):
    if not session.get('user_id'):
        return redirect(url_for('auth.Login'))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

#==================================================================================================================
@student_bp.route('/company_details/<int:company_id>', methods=['GET','POST'])
def view_company_details(company_id):

    company = companies.query.filter_by(id=company_id).first()
    active_drives = placement_drives.query.filter_by(status='approved', company_id=company_id).all()

    return render_template('/student/view_company_details.html',
    about_company=company.about_company,
    active_drives=active_drives,
    is_blacklisted=company.is_blacklisted)

#==================================================================================================================
@student_bp.route('/student/company_details/drive detail/<int:drive_id>', methods=['GET','POST'])
def company_specific_drive_detail(drive_id):
    
    drive = placement_drives.query.filter_by(id=drive_id).first()

    return render_template('/student/company_specific_drive_detail.html',
    drive_id=drive.id,
    job_id=drive.job_id,
    job_title=drive.job_title,
    job_description=drive.job_description,
    required_skills=drive.required_skills,
    experience_required=drive.experience_required,
    salary_range=drive.salary_range,
    eligibility_criteria=drive.eligibility_criteria,
    deadline=drive.deadline)

#==================================================================================================================
@student_bp.route('/student/apply_job/<int:drive_id>', methods=['GET', 'POST'])
def apply_job(drive_id):
    if not session.get('user_id'):
        return redirect(url_for('auth.Login'))

    if request.method == 'POST':
        
        #duplicate check--------------------------------------
        existing = applications.query.filter_by(
            student_id=session.get('user_id'),
            drive_id=drive_id
            ).first()
        if existing:
            return 'Already applied!' #-----------------------

        from werkzeug.utils import secure_filename

        file = request.files.get('cv')

        if not file or file.filename == '':
            return 'No file Uploaded'
        
        student_id =  session.get('user_id')

        filename = f"{student_id}_{drive_id}_{secure_filename(file.filename)}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    
        application_date = date.today()

        new_application = applications(student_id=student_id,
        drive_id=drive_id,
        cv_filename=filename,
        application_date=application_date)

        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for('student.student_application_history'))

    
    return render_template('student/apply_job.html',  drive_id=drive_id)

#==================================================================================================================
@student_bp.route('/student/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('user_id'):
        return redirect(url_for('auth.Login'))

    student = students.query.get(session['user_id'])

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        education = request.form.get('education')
        skills = request.form.get('skills')
        contact = request.form.get('contact')

        #updating data in db
        student.name = name
        student.email = email
        student.department = department
        student.education = education
        student.skills = skills
        student.contact = contact

        db.session.commit()

        return redirect(url_for('student.student_dashboard'))
    
    return render_template('student/edit_profile.html', student=student)





