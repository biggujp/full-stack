from flask import Flask, request, redirect, render_template_string, session, send_from_directory
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "hrsecret"

UPLOAD_FOLDER = "uploads"
DB_PATH = "database/job.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("database", exist_ok=True)

PER_PAGE = 5
ALLOWED_EXTENSIONS = {"pdf"}

# ---------------------
# DATABASE
# ---------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS applicant(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        nickname TEXT,
        age INTEGER,
        email TEXT UNIQUE,
        phone TEXT,
        position TEXT,
        experience TEXT,
        address TEXT,
        resume TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------------
# FILE VALIDATION
# ---------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------
# LOGIN PAGE
# ---------------------

LOGIN_HTML = """

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{
background:#f4f6f9;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}

.card{
background:white;
padding:40px;
width:100%;
max-width:350px;
border-radius:12px;
box-shadow:0 4px 15px rgba(0,0,0,0.1);
}
</style>

<div class="card">

<h3 class="text-center mb-4">Admin Login</h3>

<form method="POST">

<input class="form-control mb-3" name="user" placeholder="Username">

<input class="form-control mb-3" name="pw" type="password" placeholder="Password">

<button class="btn btn-primary w-100">Login</button>

</form>

</div>
"""


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["user"] == "admin" and request.form["pw"] == "1234":
            session["login"] = True
            return redirect("/dashboard")

    return render_template_string(LOGIN_HTML)


# ---------------------
# JOB FORM
# ---------------------

FORM_HTML = """

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:#f4f6f9;
}

.card{
background:white;
border-radius:12px;
box-shadow:0 4px 15px rgba(0,0,0,0.1);
}

.header{
display:flex;
flex-wrap:wrap;
gap:10px;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
}

</style>

<div class="container mt-5">

<div class="header">

<h2>Job Application Form</h2>

<a href="/login" class="btn btn-outline-primary">
Admin Login
</a>

</div>

<div class="card p-4">

<form method="POST" action="/apply" enctype="multipart/form-data">

<div class="row mb-3">

<div class="col-md-6">
<label>Full Name</label>
<input class="form-control" name="fullname" required>
</div>

<div class="col-md-6">
<label>Nickname</label>
<input class="form-control" name="nickname" required>
</div>

</div>

<div class="row mb-3">

<div class="col-md-4">
<label>Age</label>
<input type="number" class="form-control" name="age" required>
</div>

<div class="col-md-4">
<label>Email</label>
<input class="form-control" name="email" required>
</div>

<div class="col-md-4">
<label>Phone</label>
<input class="form-control" name="phone" required>
</div>

</div>

<div class="row mb-3">

<div class="col-md-6">
<label>Position</label>
<select class="form-control" name="position" required>
<option value="">Select Position</option>
<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>
</select>
</div>

<div class="col-md-6">
<label>Experience</label>
<input class="form-control" name="experience" required placeholder="Years of experience">
</div>

</div>

<div class="mb-3">
<label>Address</label>
<textarea class="form-control" name="address" required></textarea>
</div>

<div class="mb-3">
<label>Resume (PDF only)</label>
<input type="file" class="form-control" name="resume" accept=".pdf" required>
</div>

<button class="btn btn-success btn-lg w-100">
Submit Application
</button>

</form>

</div>

</div>
"""


@app.route("/")
def index():
    return render_template_string(FORM_HTML)


# ---------------------
# APPLY
# ---------------------

@app.route("/apply", methods=["POST"])
def apply():

    fullname = request.form.get("fullname")
    nickname = request.form.get("nickname")
    age = request.form.get("age")
    email = request.form.get("email")
    phone = request.form.get("phone")
    position = request.form.get("position")
    experience = request.form.get("experience")
    address = request.form.get("address")

    file = request.files.get("resume")

    conn = get_db()

    exist = conn.execute(
        "SELECT id FROM applicant WHERE email=?",
        (email,)
    ).fetchone()

    if exist:
        conn.close()
        return "<h2 style='text-align:center;margin-top:100px;'>You already applied.</h2>"

    filename = str(uuid.uuid4()) + ".pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    conn.execute("""
    INSERT INTO applicant
    (fullname,nickname,age,email,phone,position,experience,address,resume)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (
        fullname,
        nickname,
        age,
        email,
        phone,
        position,
        experience,
        address,
        filename
    ))

    conn.commit()
    conn.close()

    return "<h2 style='text-align:center;margin-top:100px;color:green;'>Application Submitted</h2>"


# ---------------------
# DASHBOARD
# ---------------------

DASHBOARD_HTML = """

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:#f4f6f9;
}

.card-box{
background:white;
border-radius:12px;
box-shadow:0 4px 15px rgba(0,0,0,0.1);
}

.mobile-card{
border-radius:12px;
background:white;
box-shadow:0 3px 10px rgba(0,0,0,0.08);
padding:15px;
margin-bottom:15px;
}

.mobile-label{
font-size:12px;
color:gray;
}

.mobile-value{
font-weight:500;
}

</style>

<div class="container mt-4">

<a href="/" class="btn btn-outline-primary mb-3">
Back
</a>

<h3 class="text-center mb-3">HR Dashboard</h3>

<div class="card-box p-3 mb-4 text-center">

<h6>Total Applicants</h6>
<h2>{{total}}</h2>

</div>

<form method="GET" class="row g-2 mb-3">

<div class="col-md-6">
<input class="form-control" name="search" placeholder="Search name">
</div>

<div class="col-md-2">
<button class="btn btn-primary w-100">Search</button>
</div>

</form>

<div class="card-box p-4 d-none d-md-block">

<div class="table-responsive">

<table class="table table-striped">

<thead>

<tr>
<th>ID</th>
<th>Name</th>
<th>Age</th>
<th>Phone</th>
<th>Email</th>
<th>Position</th>
<th>Experience</th>
<th>Resume</th>
<th>Action</th>
</tr>

</thead>

<tbody>

{% for a in applicants %}

<tr>

<td>{{a.id}}</td>

<td>{{a.fullname}} ({{a.nickname}})</td>

<td>{{a.age}}</td>

<td>{{a.phone}}</td>

<td>{{a.email}}</td>

<td>{{a.position}}</td>

<td>{{a.experience}}</td>

<td>

<a href="/resume/{{a.resume}}" target="_blank" class="btn btn-info btn-sm">View</a>

<a href="/download/{{a.resume}}" class="btn btn-secondary btn-sm">Download</a>

</td>

<td>

<a href="/delete/{{a.id}}" class="btn btn-danger btn-sm">Delete</a>

</td>

</tr>

{% endfor %}

</tbody>

</table>

</div>

</div>

<div class="d-md-none">

{% for a in applicants %}

<div class="mobile-card">

<div class="mobile-value mb-2">
{{a.fullname}} ({{a.nickname}})
</div>

<div class="row">

<div class="col-6">
<div class="mobile-label">Age</div>
<div class="mobile-value">{{a.age}}</div>
</div>

<div class="col-6">
<div class="mobile-label">Experience</div>
<div class="mobile-value">{{a.experience}}</div>
</div>

<div class="col-6 mt-2">
<div class="mobile-label">Phone</div>
<div class="mobile-value">{{a.phone}}</div>
</div>

<div class="col-6 mt-2">
<div class="mobile-label">Position</div>
<div class="mobile-value">{{a.position}}</div>
</div>

</div>

<div class="mt-3 d-flex gap-2">

<a href="/resume/{{a.resume}}" class="btn btn-info btn-sm w-50">
Resume
</a>

<a href="/delete/{{a.id}}" class="btn btn-danger btn-sm w-50">
Delete
</a>

</div>

</div>

{% endfor %}

</div>

<nav class="mt-3">

<ul class="pagination justify-content-center">

{% for p in pages %}

<li class="page-item">
<a class="page-link" href="/dashboard?page={{p}}">{{p}}</a>
</li>

{% endfor %}

</ul>

</nav>

</div>
"""


@app.route("/dashboard")
def dashboard():

    if not session.get("login"):
        return redirect("/login")

    page = int(request.args.get("page",1))
    search = request.args.get("search","")

    conn = get_db()

    query = "SELECT * FROM applicant WHERE fullname LIKE ? OR nickname LIKE ?"
    data = conn.execute(query,('%'+search+'%','%'+search+'%')).fetchall()

    total = len(data)

    start = (page-1)*PER_PAGE
    end = start + PER_PAGE

    applicants = data[start:end]

    pages = range(1,(total//PER_PAGE)+2)

    conn.close()

    return render_template_string(
        DASHBOARD_HTML,
        applicants=applicants,
        total=total,
        pages=pages
    )


# ---------------------
# DELETE
# ---------------------

@app.route("/delete/<id>")
def delete(id):

    conn = get_db()

    conn.execute("DELETE FROM applicant WHERE id=?",(id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------------
# RESUME VIEW
# ---------------------

@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------------------
# DOWNLOAD
# ---------------------

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# ---------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)