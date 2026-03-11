"""
seed_data.py — Run this once to populate your placement portal database.
Place this file in your project-portal-main folder and run:  python seed_data.py
"""

import sqlite3
import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

import os
os.makedirs("instance", exist_ok=True)
DB_PATH = os.path.join("instance", "database.db")

# ── DATA ────────────────────────────────────────────────────────────────────

COMPANIES = [
    ("TCS", "https://www.tcs.com", "India's largest IT services company"),
    ("Infosys", "https://www.infosys.com", "Global leader in next-gen digital services"),
    ("Wipro", "https://www.wipro.com", "Technology services and consulting company"),
    ("Google", "https://careers.google.com", "Multinational technology company"),
    ("Microsoft", "https://careers.microsoft.com", "Leading software and cloud computing company"),
    ("Amazon", "https://amazon.jobs", "Global e-commerce and cloud services giant"),
    ("Flipkart", "https://www.flipkart.com/careers", "India's leading e-commerce marketplace"),
    ("Zomato", "https://www.zomato.com/careers", "Food delivery and restaurant discovery platform"),
    ("Razorpay", "https://razorpay.com/jobs", "India's leading fintech and payments company"),
    ("HDFC Bank", "https://www.hdfcbank.com/careers", "India's largest private sector bank"),
]

STUDENTS = [
    ("Aryan Sharma",   "aryan.sharma@college.edu",   "9876543210", "CSE",  8.9),
    ("Priya Patel",    "priya.patel@college.edu",    "9876543211", "IT",   8.5),
    ("Rohit Verma",    "rohit.verma@college.edu",    "9876543212", "ECE",  7.8),
    ("Sneha Iyer",     "sneha.iyer@college.edu",     "9876543213", "CSE",  9.1),
    ("Karan Mehta",    "karan.mehta@college.edu",    "9876543214", "MECH", 7.2),
    ("Ananya Singh",   "ananya.singh@college.edu",   "9876543215", "CSE",  8.7),
    ("Dev Nair",       "dev.nair@college.edu",       "9876543216", "IT",   8.0),
    ("Pooja Joshi",    "pooja.joshi@college.edu",    "9876543217", "ECE",  7.5),
    ("Rahul Gupta",    "rahul.gupta@college.edu",    "9876543218", "CSE",  9.3),
    ("Meera Krishnan", "meera.krishnan@college.edu", "9876543219", "IT",   8.2),
    ("Aditya Rao",     "aditya.rao@college.edu",     "9876543220", "CSE",  7.9),
    ("Tanvi Desai",    "tanvi.desai@college.edu",    "9876543221", "MECH", 8.4),
    ("Vikram Bose",    "vikram.bose@college.edu",    "9876543222", "ECE",  7.6),
    ("Ishaan Malhotra","ishaan.malhotra@college.edu","9876543223", "CSE",  8.8),
    ("Riya Kapoor",    "riya.kapoor@college.edu",    "9876543224", "IT",   9.0),
]

DRIVES = [
    # (company_index, job_title, description, eligibility, package, min_cgpa, max_applicants, location, days_from_now)
    (0, "System Engineer", "Work on enterprise IT systems and client solutions.", "Any branch, CGPA ≥ 6.0", "7 LPA", 6.0, 100, "Chennai", 20),
    (0, "Business Analyst", "Analyze business requirements and provide IT solutions.", "Any branch, CGPA ≥ 6.5", "8 LPA", 6.5, 60, "Mumbai", 25),
    (1, "Software Engineer", "Build scalable backend systems and APIs.", "CSE/IT, CGPA ≥ 7.0", "12 LPA", 7.0, 40, "Bangalore", 15),
    (1, "Data Engineer", "Design and maintain data pipelines and warehouses.", "CSE/IT/ECE, CGPA ≥ 7.5", "14 LPA", 7.5, 20, "Pune", 30),
    (2, "Full Stack Developer", "Develop end-to-end web applications.", "CSE/IT, CGPA ≥ 7.0", "11 LPA", 7.0, 30, "Hyderabad", 18),
    (3, "Software Development Engineer", "Work on Google-scale infrastructure and products.", "CSE/IT, CGPA ≥ 8.0", "45 LPA", 8.0, 10, "Bangalore", 10),
    (4, "Software Engineer II", "Build features for Microsoft Azure and Office products.", "CSE/IT, CGPA ≥ 8.0", "40 LPA", 8.0, 10, "Hyderabad", 12),
    (5, "SDE-1", "Build features for Amazon's e-commerce and AWS platforms.", "CSE/IT, CGPA ≥ 7.5", "38 LPA", 7.5, 15, "Bangalore", 8),
    (6, "Software Development Engineer", "Work on Flipkart's supply chain and product teams.", "CSE/IT, CGPA ≥ 7.5", "28 LPA", 7.5, 20, "Bangalore", 22),
    (7, "Backend Engineer", "Build scalable microservices for food delivery platform.", "CSE/IT, CGPA ≥ 7.0", "22 LPA", 7.0, 25, "Gurgaon", 28),
    (8, "Frontend Engineer", "Build intuitive UX for Razorpay's payment products.", "CSE/IT, CGPA ≥ 7.5", "24 LPA", 7.5, 15, "Bangalore", 14),
    (9, "IT Analyst", "Work on HDFC's core banking and digital finance platforms.", "Any branch, CGPA ≥ 7.0", "9 LPA", 7.0, 50, "Mumbai", 35),
]

APP_STATUSES = ["Applied", "Applied", "Applied", "Shortlisted", "Rejected"]

# ── SEED ────────────────────────────────────────────────────────────────────

def seed():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")

    # Create tables
    with open("schema.sql") as f:
        con.executescript(f.read())

    print("✓ Schema created")

    # Admin
    try:
        con.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, 'admin')",
            ("admin@portal.com", generate_password_hash("admin123"))
        )
        print("✓ Admin created  →  admin@portal.com / admin123")
    except sqlite3.IntegrityError:
        print("  Admin already exists, skipping")

    # Companies
    company_ids = []
    for i, (name, website, desc) in enumerate(COMPANIES):
        email = f"{name.lower().replace(' ', '')}@company.com"
        try:
            cur = con.execute(
                "INSERT INTO users (email, password_hash, role) VALUES (?, ?, 'company')",
                (email, generate_password_hash("company123"))
            )
            user_id = cur.lastrowid
            cur2 = con.execute(
                "INSERT INTO companies (user_id, company_name, website, description, approval_status) VALUES (?, ?, ?, ?, 'Approved')",
                (user_id, name, website, desc)
            )
            company_ids.append(cur2.lastrowid)
        except sqlite3.IntegrityError:
            row = con.execute("SELECT c.id FROM companies c JOIN users u ON c.user_id=u.id WHERE u.email=?", (email,)).fetchone()
            company_ids.append(row[0] if row else None)

    print(f"✓ {len(COMPANIES)} companies inserted  →  password: company123")

    # Students
    student_ids = []
    for name, email, phone, branch, cgpa in STUDENTS:
        try:
            cur = con.execute(
                "INSERT INTO users (email, password_hash, role) VALUES (?, ?, 'student')",
                (email, generate_password_hash("student123"))
            )
            user_id = cur.lastrowid
            cur2 = con.execute(
                "INSERT INTO students (user_id, full_name, phone, branch, cgpa) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, phone, branch, cgpa)
            )
            student_ids.append(cur2.lastrowid)
        except sqlite3.IntegrityError:
            row = con.execute("SELECT s.id FROM students s JOIN users u ON s.user_id=u.id WHERE u.email=?", (email,)).fetchone()
            student_ids.append(row[0] if row else None)

    print(f"✓ {len(STUDENTS)} students inserted  →  password: student123")

    # Placement Drives
    drive_ids = []
    for (ci, title, desc, elig, pkg, min_cgpa, max_app, location, days) in DRIVES:
        deadline = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        company_id = company_ids[ci] if ci < len(company_ids) else company_ids[0]
        try:
            cur = con.execute(
                """INSERT INTO placement_drives
                   (company_id, job_title, job_description, eligibility, package, min_cgpa, max_applicants, location, application_deadline, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Approved')""",
                (company_id, title, desc, elig, pkg, min_cgpa, max_app, location, deadline)
            )
            drive_ids.append(cur.lastrowid)
        except Exception as e:
            print(f"  Drive insert error: {e}")

    print(f"✓ {len(DRIVES)} placement drives inserted")

    # Applications — each student applies to 2-4 random drives
    app_count = 0
    for sid in student_ids:
        if sid is None:
            continue
        chosen_drives = random.sample(drive_ids, min(random.randint(2, 4), len(drive_ids)))
        for did in chosen_drives:
            status = random.choice(APP_STATUSES)
            try:
                con.execute(
                    "INSERT INTO applications (student_id, drive_id, status) VALUES (?, ?, ?)",
                    (sid, did, status)
                )
                app_count += 1
            except sqlite3.IntegrityError:
                pass

    print(f"✓ {app_count} applications inserted")

    con.commit()
    con.close()

    print("\n✅ Database seeded successfully!")
    print("\nLogin credentials:")
    print("  Admin   →  admin@portal.com      / admin123")
    print("  Company →  tcs@company.com        / company123")
    print("  Student →  aryan.sharma@college.edu / student123")

if __name__ == "__main__":
    seed()
