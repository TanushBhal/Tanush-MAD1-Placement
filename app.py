import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


def create_app():
    app = Flask(__name__)
    app.secret_key = "placementparadise2024"

    os.makedirs("instance", exist_ok=True)
    app.config["DATABASE"] = os.path.join("instance", "database.db")

    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def login_required(role=None):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if "user_id" not in session:
                    return redirect("/login")
                if role and session.get("role") != role:
                    return render_template("errors/403.html")
                return f(*args, **kwargs)
            return wrapper
        return decorator

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/create-admin")
    def create_admin():
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                ("admin@placementparadise.com", generate_password_hash("admin@123"), "admin")
            )
            db.commit()
            return "Admin created successfully!"
        except:
            return "Admin already exists."

    @app.route("/init-db")
    def init_db():
        db = get_db()
        with open("schema.sql") as f:
            db.executescript(f.read())
        db.commit()
        return "Database initialized!"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["role"] = user["role"]
                if user["role"] == "admin":
                    return redirect("/admin-dashboard")
                elif user["role"] == "company":
                    company = db.execute("SELECT * FROM companies WHERE user_id=?", (user["id"],)).fetchone()
                    if company["approval_status"] != "Approved":
                        flash("Your company account is pending admin approval.", "warning")
                        return redirect("/login")
                    return redirect("/company-dashboard")
                else:
                    return redirect("/student-dashboard")
            else:
                flash("Invalid email or password.", "danger")
        return render_template("auth/login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")

    @app.route("/register-student", methods=["GET", "POST"])
    def register_student():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            full_name = request.form["full_name"]
            branch = request.form["branch"]
            db = get_db()
            try:
                cursor = db.execute(
                    "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                    (email, generate_password_hash(password), "student")
                )
                db.execute(
                    "INSERT INTO students (user_id, full_name, branch) VALUES (?, ?, ?)",
                    (cursor.lastrowid, full_name, branch)
                )
                db.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect("/login")
            except:
                flash("An account with this email already exists.", "danger")
        return render_template("auth/register_student.html")

    @app.route("/register-company", methods=["GET", "POST"])
    def register_company():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            company_name = request.form["company_name"]
            website = request.form["website"]
            db = get_db()
            try:
                cursor = db.execute(
                    "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                    (email, generate_password_hash(password), "company")
                )
                db.execute(
                    "INSERT INTO companies (user_id, company_name, website, approval_status) VALUES (?, ?, ?, ?)",
                    (cursor.lastrowid, company_name, website, "Pending")
                )
                db.commit()
                flash("Company registered. Await admin approval before logging in.", "success")
                return redirect("/login")
            except:
                flash("An account with this email already exists.", "danger")
        return render_template("auth/register_company.html")

    @app.route("/admin-dashboard")
    @login_required(role="admin")
    def admin_dashboard():
        db = get_db()
        students_count = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        companies_count = db.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
        drives_count = db.execute("SELECT COUNT(*) FROM placement_drives").fetchone()[0]
        applications_count = db.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        companies_list = db.execute(
            """SELECT c.id, c.company_name, c.website, c.approval_status, c.created_at, u.email
               FROM companies c
               INNER JOIN users u ON c.user_id = u.id
               ORDER BY c.created_at DESC"""
        ).fetchall()
        students_list = db.execute(
            """SELECT s.id, s.full_name, s.branch, s.cgpa, s.phone, s.created_at, u.email
               FROM students s
               INNER JOIN users u ON s.user_id = u.id
               ORDER BY s.created_at DESC"""
        ).fetchall()
        return render_template(
            "admin/dashboard.html",
            students=students_count,
            companies=companies_count,
            drives=drives_count,
            applications=applications_count,
            companies_list=companies_list,
            students_list=students_list,
        )

    @app.route("/admin/companies")
    @login_required(role="admin")
    def view_companies():
        db = get_db()
        companies = db.execute(
            "SELECT * FROM companies WHERE approval_status = 'Pending'"
        ).fetchall()
        return render_template("admin/view_companies.html", companies=companies)

    @app.route("/admin/approve-company/<int:company_id>")
    @login_required(role="admin")
    def approve_company(company_id):
        db = get_db()
        db.execute("UPDATE companies SET approval_status = 'Approved' WHERE id = ?", (company_id,))
        db.commit()
        return redirect("/admin/companies")

    @app.route("/admin/drives")
    @login_required(role="admin")
    def view_drives():
        db = get_db()
        drives = db.execute(
            """SELECT pd.*, c.company_name
               FROM placement_drives pd
               JOIN companies c ON pd.company_id = c.id
               WHERE pd.status = 'Pending'"""
        ).fetchall()
        return render_template("admin/view_drives.html", drives=drives)

    @app.route("/admin/approve-drive/<int:drive_id>")
    @login_required(role="admin")
    def approve_drive(drive_id):
        db = get_db()
        db.execute("UPDATE placement_drives SET status = 'Approved' WHERE id = ?", (drive_id,))
        db.commit()
        return redirect("/admin/drives")

    @app.route("/company-dashboard")
    @login_required(role="company")
    def company_dashboard():
        db = get_db()
        company = db.execute("SELECT * FROM companies WHERE user_id=?", (session["user_id"],)).fetchone()
        drives = db.execute("SELECT * FROM placement_drives WHERE company_id=?", (company["id"],)).fetchall()
        return render_template("company/dashboard.html", company=company, drives=drives)

    @app.route("/company/create-drive", methods=["GET", "POST"])
    @login_required(role="company")
    def create_drive():
        if request.method == "POST":
            db = get_db()
            company = db.execute("SELECT * FROM companies WHERE user_id = ?", (session["user_id"],)).fetchone()
            db.execute(
                """INSERT INTO placement_drives
                   (company_id, job_title, job_description, eligibility, package, location, application_deadline, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (company["id"], request.form["job_title"], request.form["job_description"],
                 request.form["eligibility"], request.form["package"],
                 request.form["location"], request.form["deadline"], "Pending")
            )
            db.commit()
            flash("Drive submitted for admin approval.", "success")
            return redirect("/company-dashboard")
        return render_template("company/create_drive.html")

    @app.route("/student-dashboard")
    @login_required(role="student")
    def student_dashboard():
        db = get_db()
        student = db.execute("SELECT * FROM students WHERE user_id=?", (session["user_id"],)).fetchone()
        total = db.execute("SELECT COUNT(*) FROM applications WHERE student_id=?", (student["id"],)).fetchone()[0]
        shortlisted = db.execute("SELECT COUNT(*) FROM applications WHERE student_id=? AND status='Shortlisted'", (student["id"],)).fetchone()[0]
        rejected = db.execute("SELECT COUNT(*) FROM applications WHERE student_id=? AND status='Rejected'", (student["id"],)).fetchone()[0]
        return render_template("student/dashboard.html", student=student, total=total, shortlisted=shortlisted, rejected=rejected)

    @app.route("/student/drives")
    @login_required(role="student")
    def student_drives():
        db = get_db()
        drives = db.execute(
            """SELECT pd.*, c.company_name
               FROM placement_drives pd
               JOIN companies c ON pd.company_id = c.id
               WHERE pd.status = 'Approved'"""
        ).fetchall()
        return render_template("student/view_drives.html", drives=drives)

    @app.route("/student/apply/<int:drive_id>")
    @login_required(role="student")
    def apply_drive(drive_id):
        db = get_db()
        student = db.execute("SELECT * FROM students WHERE user_id = ?", (session["user_id"],)).fetchone()
        existing = db.execute(
            "SELECT * FROM applications WHERE student_id = ? AND drive_id = ?",
            (student["id"], drive_id)
        ).fetchone()
        if existing:
            return render_template("student/already_applied.html")
        db.execute(
            "INSERT INTO applications (student_id, drive_id, status) VALUES (?, ?, ?)",
            (student["id"], drive_id, "Applied")
        )
        db.commit()
        return render_template("student/apply_success.html")

    @app.route("/student/applications")
    @login_required(role="student")
    def student_applications():
        db = get_db()
        student = db.execute("SELECT * FROM students WHERE user_id = ?", (session["user_id"],)).fetchone()
        applications = db.execute(
            """SELECT a.*, pd.job_title, c.company_name
               FROM applications a
               JOIN placement_drives pd ON a.drive_id = pd.id
               JOIN companies c ON pd.company_id = c.id
               WHERE a.student_id = ?""",
            (student["id"],)
        ).fetchall()
        return render_template("student/applications.html", applications=applications)

    @app.route("/student/profile", methods=["GET", "POST"])
    @login_required(role="student")
    def student_profile():
        db = get_db()
        student = db.execute("SELECT * FROM students WHERE user_id=?", (session["user_id"],)).fetchone()
        if request.method == "POST":
            db.execute("UPDATE students SET cgpa=? WHERE id=?", (request.form["cgpa"], student["id"]))
            db.commit()
            flash("Profile updated successfully.", "success")
            return redirect("/student/profile")
        return render_template("student/profile.html", student=student)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
