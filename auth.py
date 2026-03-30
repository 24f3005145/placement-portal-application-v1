from flask import Blueprint, render_template, request, redirect, session, url_for
from models import students, companies, db
from werkzeug.security import check_password_hash
from sqlalchemy import func
from config import ADMIN_EMAIL, ADMIN_PASSWORD

auth_bp = Blueprint('auth', __name__)

#LOGIN================================================================================================================
@auth_bp.route('/login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':

        #adding admin functionality
        email = request.form.get('email')
        student_password = request.form.get('student_password')
        company_name = request.form.get('company_name')
        hirer_password =  request.form.get('hirer_password')

        if (email == ADMIN_EMAIL and student_password == ADMIN_PASSWORD) or (company_name == ADMIN_EMAIL and hirer_password == ADMIN_PASSWORD):
            session.clear()             #fix for old session usage issue
            session['admin'] = True
            return redirect(url_for('admin.admin_dashboard'))


        type_of_user_login = request.form.get('role')

        if(type_of_user_login == 'student'):
            if not email or not student_password:
                return render_template('login.html', error="Please fill all fields!", color='red')

            user = students.query.filter_by(email=email).first()

            if user and user.check_password(student_password):
                if user.is_active == 1:
                    session.clear()         #fix for old session usage issue
                    session['user_id'] = user.id
                    return redirect(url_for('student.student_dashboard'))
                else:
                    return render_template('login.html', error="You have been debarred from the placement portal !", color='red')

            else:
                return render_template('login.html', error="Invalid student name or password.", color='red')



        elif(type_of_user_login == 'hirer'):
            if not company_name or not hirer_password:
                return render_template('login.html', error="Please fill all fields!", color='red')

            user = companies.query.filter(func.lower(companies.company_name) == company_name.lower()).first()

            if user and user.check_password(hirer_password):
                if user.status_of_approval() == 'pending':
                    return render_template('login.html', error="Your company has been succesfully listed. dashboard will be available after admin approval !", color='green')
                elif user.status_of_approval() == 'rejected':
                    return render_template('login.html', error="Your company listing has been rejected!", color='red')
                elif user.is_blacklisted:
                    return render_template('login.html', error="Your Company has been blacklisted!", color='red')
                else:
                    session.clear()         #fix for old session usage issue
                    session['company_name'] = user.company_name
                    return redirect(url_for('company.company_dashboard', name=company_name))
            else:
                return render_template('login.html', error="Invalid company name or password.", color='red')
    
    else:
        return render_template('login.html')



#REGISTER=============================================================================================================
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        type_of_user_login = request.form.get('role')

        if(type_of_user_login == 'student'):
            name = request.form.get('name')
            email = request.form.get('email')
            department = request.form.get('department')
            password = request.form.get('student_password')

            student = students.query.filter_by(email=email).first()

            if student:
                return render_template('already_exists.html')
            else:
                new_student = students(name=name, email=email, role=type_of_user_login, department=department)
                new_student.set_password(password)

                db.session.add(new_student)
                db.session.commit()
                
                return render_template('login.html', error="you have been successfully registered, Try Logging in !!", color='green')




        if(type_of_user_login == 'hirer'):
            company_name = request.form.get('company_name')
            hr_contact = request.form.get('hr_contact')
            website = request.form.get('website')
            about_company = request.form.get('about_company')
            password = request.form.get('hirer_password').strip()

            company = companies.query.filter_by(company_name=company_name).first()

            if company:
                return render_template('already_exists.html')
            else:
                new_company = companies(company_name=company_name, hr_contact=hr_contact, website=website, about_company=about_company)
                new_company.set_password(password=password)

                db.session.add(new_company)
                db.session.commit()
                
                return render_template('login.html', error="Your company has been succesfully listed. dashboard will be available after admin approval !", color='green')
                
    else:
        return render_template('register.html')


#Logout==============================================================================================================
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.Login'))



