from app import app
from models import db, students, companies, placement_drives, applications
from datetime import datetime, date

with app.app_context():

    print("🔄 Seeding database...")

    # ------------------ Clear Existing Data ------------------
    db.session.query(applications).delete()
    db.session.query(placement_drives).delete()
    db.session.query(students).delete()
    db.session.query(companies).delete()
    db.session.commit()

    # ------------------ Students ------------------
    s1 = students(name="Rahul Sharma", email="rahul@gmail.com", department="CSE",
                  role="student", is_active=1, education="B.Tech CSE",
                  skills="Python, Flask, SQL", contact="9876543210")
    s1.set_password("123456")

    s2 = students(name="Priya Singh", email="priya@gmail.com", department="IT",
                  role="student", is_active=1, education="B.Tech IT",
                  skills="Java, Spring Boot", contact="9123456780")
    s2.set_password("123456")

    s3 = students(name="Aman Verma", email="aman@gmail.com", department="ECE",
                  role="student", is_active=1, education="B.Tech ECE",
                  skills="C++, Embedded Systems", contact="9988776655")
    s3.set_password("123456")

    s4 = students(name="Neha Gupta", email="neha@gmail.com", department="CSE",
                  role="student", is_active=1, education="B.Tech CSE",
                  skills="React, Node.js", contact="9012345678")
    s4.set_password("123456")

    db.session.add_all([s1, s2, s3, s4])
    db.session.commit()

    # ------------------ Companies ------------------
    c1 = companies(company_name="TCS", hr_contact="hr@tcs.com",
                   website="https://www.tcs.com",
                   about_company="Leading IT services company",
                   approval_status="approved", is_blacklisted=0)
    c1.set_password("123456")

    c2 = companies(company_name="Infosys", hr_contact="hr@infosys.com",
                   website="https://www.infosys.com",
                   about_company="Global consulting company",
                   approval_status="approved", is_blacklisted=0)
    c2.set_password("123456")

    c3 = companies(company_name="Wipro", hr_contact="hr@wipro.com",
                   website="https://www.wipro.com",
                   about_company="IT and consulting services",
                   approval_status="approved", is_blacklisted=0)
    c3.set_password("123456")

    c4 = companies(company_name="Google", hr_contact="hr@google.com",
                   website="https://www.google.com",
                   about_company="Product based tech giant",
                   approval_status="approved", is_blacklisted=0)
    c4.set_password("123456")

    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    # ------------------ Placement Drives ------------------
    d1 = placement_drives(company_id=c1.id, job_id=101,
                          job_title="Software Engineer",
                          job_description="Backend development using Python",
                          required_skills="Python, Flask, SQL",
                          experience_required="0-1 years",
                          salary_range="6-8 LPA",
                          eligibility_criteria="CSE/IT with CGPA > 7",
                          deadline=date(2026, 4, 10),
                          status="approved")

    d2 = placement_drives(company_id=c2.id, job_id=102,
                          job_title="Data Analyst",
                          job_description="SQL and dashboards",
                          required_skills="SQL, Excel, Python",
                          experience_required="0-2 years",
                          salary_range="5-7 LPA",
                          eligibility_criteria="All branches with CGPA > 6.5",
                          deadline=date(2026, 4, 12),
                          status="approved")

    d3 = placement_drives(company_id=c3.id, job_id=103,
                          job_title="System Engineer",
                          job_description="Support and system ops",
                          required_skills="Linux, Networking",
                          experience_required="0-1 years",
                          salary_range="4-6 LPA",
                          eligibility_criteria="All branches",
                          deadline=date(2026, 4, 15),
                          status="approved")

    d4 = placement_drives(company_id=c4.id, job_id=104,
                          job_title="SDE Intern",
                          job_description="Work on scalable systems",
                          required_skills="DSA, Python, C++",
                          experience_required="0 years",
                          salary_range="Internship",
                          eligibility_criteria="CSE/IT with strong DSA",
                          deadline=date(2026, 4, 20),
                          status="approved")

    db.session.add_all([d1, d2, d3, d4])
    db.session.commit()

    # ------------------ Applications ------------------
    today = str(datetime.now().date())

    a1 = applications(student_id=s1.id, drive_id=d1.id,
                      application_date=today, cv_filename="rahul_cv.pdf",
                      status="applied")

    a2 = applications(student_id=s2.id, drive_id=d2.id,
                      application_date=today, cv_filename="priya_cv.pdf",
                      status="shortlisted")

    a3 = applications(student_id=s3.id, drive_id=d3.id,
                      application_date=today, cv_filename="aman_cv.pdf",
                      status="rejected")

    a4 = applications(student_id=s4.id, drive_id=d4.id,
                      application_date=today, cv_filename="neha_cv.pdf",
                      status="selected")

    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()

    print("✅ Database seeded with 4 entries each!")