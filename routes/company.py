from flask import Blueprint, render_template, request, redirect, session, url_for, send_from_directory
from models import companies, placement_drives, applications, db
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

company_bp = Blueprint('company', __name__)

#Company routes=========================================================================================================
@company_bp.route('/company/<name>', methods=['GET','POST'])
def company_dashboard(name):
    if not session.get('company_name'):
        return redirect(url_for('auth.Login'))
    if session.get('company_name') != name:
        return "Unauthorized"
    
    company = companies.query.filter_by(company_name=name).first()
    
    if not company:
        return "Company not found"
    
    active_jobs = placement_drives.query.filter_by(company_id=company.id, status='approved').all()
    
    return render_template('company/company_dashboard.html', name=name, 
    active_jobs=active_jobs, company_id=company.id)  #redirected from login

#====================================================================================================================
@company_bp.route('/company/action', methods=['GET', 'POST'])
def company_action():
    if not session.get('company_name'):
        return redirect(url_for('auth.Login'))

    action = request.form.get('action')
    
    if action == 'complete_drive':
        job = placement_drives.query.get(request.form.get('job_id'))
        job.status = 'complete'
    
    db.session.commit()
    return redirect(url_for('company.company_dashboard', name=session['company_name']))

#====================================================================================================================
@company_bp.route('/company/<name>/post_job', methods=['GET','POST'])
def post_job(name):
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        required_skills = request.form.get('required_skills')
        experience_required = request.form.get('experience_required')
        salary_range = request.form.get('salary_range')
        eligibility_criteria = request.form.get('eligibility_criteria')
        
        deadline = datetime.strptime(request.form.get('deadline'), "%Y-%m-%d").date()   #date

        drive_check = placement_drives.query.filter_by(job_id=job_id).first()

        company = companies.query.filter_by(company_name=session['company_name']).first()

        if drive_check:
            return render_template('already_exists.html')
        else:
            new_drive = placement_drives(job_id = job_id,
            company_id=company.id,
            job_title = job_title,
            job_description = job_description,
            required_skills = required_skills,
            experience_required = experience_required,
            salary_range = salary_range,
            eligibility_criteria = eligibility_criteria,
            deadline = deadline)

            db.session.add(new_drive)
            db.session.commit()

            return redirect(url_for('company.company_dashboard', name=session['company_name']))
        
    else:
        return redirect(request.referrer)

#====================================================================================================================
@company_bp.route('/company/job/<int:drive_id>')
def job_details(drive_id):
    if not session.get('company_name'):
        return redirect(url_for('auth.Login'))
    
    job = placement_drives.query.get(drive_id)

    job_applications = applications.query.filter_by(drive_id=drive_id).all()

    applied_count = applications.query.filter_by(drive_id=drive_id, status='applied').count()
    shortlisted_count = applications.query.filter_by(drive_id=drive_id, status='shortlisted').count()
    selected_count = applications.query.filter_by(drive_id=drive_id, status='selected').count()

    return render_template('company/job_details.html',
    job=job,
    job_applications=job_applications,
    applied_count=applied_count,
    shortlisted_count=shortlisted_count,
    selected_count=selected_count)

#====================================================================================================================
@company_bp.route('/company/application/update', methods=['POST'])
def update_application_status():
    if not session.get('company_name'):
        return redirect(url_for('auth.Login'))
    
    action = request.form.get('action')

    if action == 'Shortlist':
        application = applications.query.get(request.form.get('application_id'))
        application.status = 'shortlisted'
    elif action == 'Select':
        application = applications.query.get(request.form.get('application_id'))
        application.status = 'selected'
    elif action == 'Reject':
        application = applications.query.get(request.form.get('application_id'))
        application.status = 'rejected'

    db.session.commit()
    return redirect(request.referrer)

#====================================================================================================================
@company_bp.route('/company/view_cv/<filename>')
def company_view_cv(filename):
    if not session.get('company_name'):
        return redirect(url_for('auth.Login'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


