# Placement Portal Application

A full-stack web application built using Flask that simulates a college placement system where students can apply for jobs and companies can manage hiring.

-----------------------------------------------------------------------------------------------------------------------------------------------

## Features

### 👨‍🎓 Student

- Register and login securely
- Update profile (department, skills, resume upload)
- View and search available placement drives
- Apply to jobs/placement drives
- Track application status (applied / shortlisted / rejected / selected)

---

### 🏢 Company

- Register and login
- Create and manage placement drives/job postings
- View applicants for each drive
- Update application status (shortlist / reject / select)

---

### 🛠️ Admin

- Manage students and companies
- Approve or monitor placement drives
- View all applications
- Monitor system activity

-----------------------------------------------------------------------------------------------------------------------------------------------

## Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML, CSS, Jinja2
* **Authentication:** Session-based login, Werkzueg Security

-----------------------------------------------------------------------------------------------------------------------------------------------

## 📁 Project Structure
```
placement-portal-application-v1/
│
├── app.py
├── models.py
├── config.py
│
├── routes/
│   ├── admin.py
│   ├── auth.py
│   ├── company.py
│   └── student.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── error.html
│   ├── success.html
│   ├── already_exists.html
│   │
│   ├── admin/
│   │   ├── admin_dashboard.html
│   │   └── student_application_viewAs_admin.html
│   │
│   ├── company/
│   │   ├── company_dashboard.html
│   │   └── job_details.html
│   │
│   └── student/
│       ├── student_dashboard.html
│       ├── company_specific_drive_detail.html
│       ├── apply_job.html
│       ├── edit_profile.html
│       ├── student_application_history.html
│       └── view_company_details.html
│
├── static/
│   └── css/
│       ├── style.css
│       │
│       ├── admin/
│       │   └── admin_dashboard.css
│       │
│       ├── company/
│       │   ├── company_dashboard.css
│       │   └── job_details.css
│       │
│       └── student/
│           ├── student_dashboard.css
│           ├── view_company_details.css
│           ├── student_application_history.css
│           ├── edit_profile.css
│           └── company_specific_drive_detail.css
│
├── instance/          # Database files
│   └── new.db
│
└── uploads/           # User uploaded resumes
```
-----------------------------------------------------------------------------------------------------------------------------------------------

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/24f3005145/placement-portal-application-v1.git
cd placement-portal-application-v1
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate it:

* Windows:

```
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the Application

```
python app.py
```

App will run on:

```
http://127.0.0.1:5000/
```

---

## 🧪 Test Data (Important)

Use command :

``` 
python seed.py 

``` 
to feed the test data into the database.

-----------------------------------------------------------------------------------------------------------------------------------------------

## 💼 Why This Project Matters

This project demonstrates:

* Full-stack development skills
* Database design (relationships, queries)
* Authentication system
* Real-world use case (placement portal system)

-----------------------------------------------------------------------------------------------------------------------------------------------

## Author

Shubhankar Bajpai, 
Data Science Student (IIT Madras)

-----------------------------------------------------------------------------------------------------------------------------------------------

## for Recruiters

This project can be extended into a scalable placement platform with:

* Microservices architecture
* React frontend
* Cloud deployment and many more possibilties and features...


-----------------------------------------------------------------------------------------------------------------------------------------------

