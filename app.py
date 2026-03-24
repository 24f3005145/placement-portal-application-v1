from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import db
from models import students, companies, placement_drives, applications

from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


ADMIN_EMAIL = 'admin123@gmail.com'
ADMIN_PASSWORD = 'admin123'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/company/<name>', methods=['GET','POST'])
def company_dashboard(name):
    return render_template('company/company_dashboard.html', name=name)



#admin 1st view page --------------------------------------------------------- 'might change later'
@app.route('/admin', methods=['GET','POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('Login'))

    if request.method == 'GET':
        student_query = request.args.get('student_query')
        if student_query:
            active_students = students.query.filter(
            (students.name.ilike(f"%{student_query}%")) |
            (students.email.ilike(f"%{student_query}%")) |
            (students.id == student_query
            )).all()
        else:
            active_students = students.query.filter_by(is_active=1).all()

        company_query = request.args.get('company_query')
        if company_query:
            registered_companies = companies.query.filter(
            (companies.company_name.ilike(f"%{company_query}%")) |
            (companies.website.ilike(f"%{company_query}%"))
            ).all()
        else:
            registered_companies = companies.query.filter_by(approval_status='approved').all()


        pending_companies = companies.query.filter_by(approval_status='pending').all()
        
        drives = placement_drives.query.filter_by(status='approved')
        return render_template('admin/admin_dashboard.html', 
        pending_companies=pending_companies, 
        registered_companies=registered_companies, 
        active_students=active_students,
        drives=drives)


#admin actions
@app.route('/admin/action', methods=['GET', 'POST'])
def admin_action():
    if not session.get('admin'):
        return redirect(url_for('Login'))

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
            drive.status = 'closed'
    
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
    elif action == 'close_drive':
        placement_drive = placement_drives.query.get(request.form.get('drive_id'))
        placement_drive.status = 'closed'

    db.session.commit()
    return redirect(url_for('admin_dashboard'))

    




#login
@app.route('/login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':

        #adding admin functionality
        email = request.form.get('email')
        student_password = request.form.get('student_password')
        company_name = request.form.get('company_name')
        hirer_password =  request.form.get('hirer_password')

        if (email == ADMIN_EMAIL and student_password == ADMIN_PASSWORD) or (company_name == ADMIN_EMAIL and hirer_password == ADMIN_PASSWORD):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))


        type_of_user_login = request.form.get('role')

        if(type_of_user_login == 'student'):
            #email = request.form.get('email')
            #student_password = request.form.get('student_password')
            
            if not email or not student_password:
                return render_template('login.html', error="Please fill all fields!", color='red')

            user = students.query.filter_by(email=email).first()

            if user and user.check_password(student_password):
                session['email'] = email
                return render_template('success.html')
                #return redirect(url_for('students_dasboard'))
            else:
                return render_template('login.html', error="Invalid student name or password.", color='red')



        elif(type_of_user_login == 'hirer'):
            #company_name = request.form.get('company_name').strip()
            #hirer_password =  request.form.get('hirer_password').strip()
            
            if not company_name or not hirer_password:
                return render_template('login.html', error="Please fill all fields!", color='red')

            user = companies.query.filter(func.lower(companies.company_name) == company_name.lower()).first()

            if user and user.check_password(hirer_password):
                if user.status_of_approval() == 'pending':
                    return render_template('login.html', error="Your company has been succesfully listed. dashboard will be available after admin approval !", color='green')
                elif user.status_of_approval() == 'rejected':
                    return render_template('login.html', error="Your company listing has been rejected by the admin !", color='red')
                elif user.is_blacklisted:
                    return render_template('login.html', error="Company is blacklisted!", color='red')
                else:
                    session['company_name'] = company_name
                    #return render_template('success.html')
                    return redirect(url_for('company_dashboard', name=company_name))
            else:
                return render_template('login.html', error="Invalid company name or password.", color='red')
    
    else:
        return render_template('login.html')
    
    


#Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        type_of_user_login = request.form.get('role')

        if(type_of_user_login == 'student'):
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('student_password')

            student = students.query.filter_by(email=email).first()

            if student:
                return render_template('already_exists.html')
            else:
                new_student = students(name=name, email=email, role=type_of_user_login)
                new_student.set_password(password)

                db.session.add(new_student)
                db.session.commit()
                session['name'] = name
                return render_template('success.html')
                #return redirect(url_for('students_dasboard'))




        if(type_of_user_login == 'hirer'):
            company_name = request.form.get('company_name')
            hr_contact = request.form.get('hr_contact')
            website = request.form.get('website')
            password = request.form.get('hirer_password').strip()

            company = companies.query.filter_by(company_name=company_name).first()

            if company:
                return render_template('already_exists.html')
            else:
                new_company = companies(company_name=company_name, hr_contact=hr_contact, website=website)
                new_company.set_password(password=password)

                db.session.add(new_company)
                db.session.commit()



                #session['company_name'] = company_name                                           
                return render_template('login.html', error="Your company has been succesfully listed. dashboard will be available after admin approval !", color='green')
                #return redirect(url_for('company_dasboard'))
    else:
        return render_template('register.html')


            
#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Login'))
    
    



db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)