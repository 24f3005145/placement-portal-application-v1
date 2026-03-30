from flask import Blueprint, render_template, request, redirect, session, url_for
from models import students, companies, placement_drives, applications, db
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__)

#Admin routes ======================================================================================================
@admin_bp.route('/admin', methods=['GET','POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('auth.Login'))

    if request.method == 'GET':

        #search functionality for student and company___________________________
        student_query = request.args.get('student_query')
        if student_query:
            active_students = students.query.filter(
            (students.name.ilike(f"%{student_query}%")) |
            (students.email.ilike(f"%{student_query}%")) |
            (students.id == student_query
            )).all()
            student_count = len(active_students)
        else:
            active_students = students.query.filter_by(is_active=1).all()
            student_count = students.query.filter_by(is_active=1).count()

        company_query = request.args.get('company_query')
        if company_query:
            registered_companies = companies.query.filter(
            (companies.company_name.ilike(f"%{company_query}%")) |
            (companies.website.ilike(f"%{company_query}%"))
            ).all()
            company_count = companies.query.filter(
            (companies.company_name.ilike(f"%{company_query}%")) |
            (companies.website.ilike(f"%{company_query}%"))
            ).count()
        else:
            registered_companies = companies.query.filter_by(approval_status='approved').all()
            company_count = companies.query.filter_by(approval_status='approved', is_blacklisted=0).count()
        #_______________________________________________________________________

        drives = placement_drives.query.filter_by(status='approved').all()
        drive_count = placement_drives.query.filter_by(status='approved').count()

        pending_companies = companies.query.filter_by(approval_status='pending').all()
        pending_drives = placement_drives.query.filter_by(status='pending').all()
        applications_list = applications.query.all()
        application_count = applications.query.count()
        
        return render_template('admin/admin_dashboard.html', 
        pending_companies=pending_companies, 
        registered_companies=registered_companies,
        company_count=company_count, 
        active_students=active_students,
        student_count=student_count,
        drives=drives,
        drive_count=drive_count,
        pending_drives=pending_drives,
        applications=applications_list,
        application_count=application_count)

#====================================================================================================================
#admin actions
@admin_bp.route('/admin/action', methods=['GET', 'POST'])
def admin_action():
    if not session.get('admin'):
        return redirect(url_for('auth.Login'))

    action = request.form.get('action')

    #company action----------
    if action == 'approve_company':
        company = companies.query.get(request.form.get('company_id'))
        company.approval_status = 'approved'
    elif action == 'reject_company':
        company = companies.query.get(request.form.get('company_id'))
        company.approval_status = 'rejected'
    elif action == 'blacklist_company':
        company = companies.query.get(request.form.get('company_id'))
        company.is_blacklisted = 1

        # cancel all drives
        for drive in company.placement_drives:
            drive.status = 'complete'
    
    #student action----------
    elif action == 'blacklist_student':
        student = students.query.get(request.form.get('student_id'))
        student.is_active = 0

    #drive action----------
    elif action == 'approve_drive':
        placement_drive = placement_drives.query.get(request.form.get('drive_id'))
        placement_drive.status = 'approved'
    elif action == 'reject_drive':
        placement_drive = placement_drives.query.get(request.form.get('drive_id'))
        placement_drive.status = 'rejected'
    elif action == 'emergency_close_drive':
        placement_drive = placement_drives.query.get(request.form.get('drive_id'))
        placement_drive.status = 'complete' 

    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))


#====================================================================================================================
@admin_bp.route('/admin/view_application/<int:student_id>/<int:drive_id>', methods=['GET'])
def student_application_viewAs_admin(student_id, drive_id):
    if not session.get('admin'):
        return redirect(url_for('auth.Login'))

    student = students.query.filter_by(id=student_id).first()
    drive = placement_drives.query.filter_by(id=drive_id).first()
    
    return render_template('admin/student_application_viewAs_admin.html', student=student, drive=drive)



