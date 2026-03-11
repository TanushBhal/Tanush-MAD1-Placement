<div align="center">

<br/>

```
██████╗ ██╗      █████╗  ██████╗███████╗███╗   ███╗███████╗███╗   ██╗████████╗
██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
██████╔╝██║     ███████║██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   
██╔═══╝ ██║     ██╔══██║██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   
██║     ███████╗██║  ██║╚██████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   
╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝  
                                                                                 
██████╗  █████╗ ██████╗  █████╗ ██████╗ ██╗███████╗███████╗                    
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██╔════╝                    
██████╔╝███████║██████╔╝███████║██║  ██║██║███████╗█████╗                      
██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║  ██║██║╚════██║██╔══╝                      
██║     ██║  ██║██║  ██║██║  ██║██████╔╝██║███████║███████╗                    
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚══════╝                   
```

### 🎓 Campus Recruitment, Reimagined.

**A full-stack web platform connecting students, companies, and admins for seamless campus placements.**

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00e5c0?style=for-the-badge)

<br/>

</div>

---

## 📌 Overview

**Placement Paradise** is a multi-role campus placement management portal built with Flask and SQLite. It handles the complete placement lifecycle — from student registration and company onboarding to admin approval workflows and application tracking.

> Built as part of the IIT Madras BS Degree App Development project.

---

## ✨ Features

### 👤 Student
- Register and manage academic profile (branch, CGPA)
- Browse all approved placement drives
- Apply to drives with one click
- Track application status (Applied / Shortlisted / Rejected)

### 🏢 Company
- Register and await admin approval
- Post placement drives with job details, eligibility, package, and deadline
- Manage all posted drives from dashboard

### ⚙️ Admin
- Approve or reject company registrations
- Approve or reject placement drives
- View all registered students and companies
- Full portal oversight from a single dashboard

---

## 🗂️ Project Structure

```
placement-paradise/
│
├── app.py                  # Main Flask application & all routes
├── config.py               # App configuration
├── schema.sql              # Database schema
├── seed_data.py            # Script to populate demo data
├── requirements.txt        # Python dependencies
│
├── instance/
│   └── database.db         # SQLite database (auto-created)
│
├── static/
│   └── css/
│       └── style.css       # Custom dark theme styles
│
├── templates/
│   ├── base.html           # Base layout with navbar
│   ├── home.html           # Landing page
│   ├── auth/               # Login & registration pages
│   ├── student/            # Student dashboard, drives, profile
│   ├── company/            # Company dashboard, create drive
│   └── admin/              # Admin dashboard, approvals
│
└── models/
    └── __init__.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite (via `sqlite3`) |
| Auth | Werkzeug password hashing, Flask sessions |
| Frontend | Jinja2 templates, Bootstrap 5.3 |
| Fonts | Syne + DM Sans (Google Fonts) |
| Styling | Custom CSS with dark theme & CSS variables |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/placement-paradise.git
cd placement-paradise
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the database
```bash
python seed_data.py
```
This creates the database, runs the schema, inserts demo companies, students, and drives.

### 4. Run the app
```bash
python app.py
```

Visit `http://127.0.0.1:5001` in your browser.

---

## 🔐 Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@portal.com | admin |
| Company | tcs@company.com | company |
| Student | aryan.sharma@college.edu | student |



---

## 🗄️ Database Schema

```
users ──────────────────────────────────────────────────
  id, email, password_hash, role, is_active, created_at

students ───────────────────────────────────────────────
  id, user_id (FK), full_name, phone, branch, cgpa

companies ──────────────────────────────────────────────
  id, user_id (FK), company_name, website, approval_status

placement_drives ───────────────────────────────────────
  id, company_id (FK), job_title, job_description,
  eligibility, package, location, deadline, status

applications ───────────────────────────────────────────
  id, student_id (FK), drive_id (FK), status, applied_at
```
---

## 📄 License

This project is for educational purposes as part of the IIT Madras BS Degree program.

---
