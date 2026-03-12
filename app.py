from flask import Flask, request, redirect, render_template_string, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "hrsecret"

UPLOAD_FOLDER = "uploads"
DB_PATH = "database/job.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("database", exist_ok=True)

PER_PAGE = 5

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
# LOGIN PAGE
# ---------------------

LOGIN_HTML = """

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
width:350px;
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
# JOB APPLICATION FORM
# ---------------------

FORM_HTML = """

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

<div class="col">
<label>Full Name</label>
<input class="form-control" name="fullname" required>
</div>

<div class="col">
<label>Nickname</label>
<input class="form-control" name="nickname">
</div>

</div>

<div class="row mb-3">

<div class="col">
<label>Email</label>
<input class="form-control" name="email" required>
</div>

<div class="col">
<label>Phone</label>
<input class="form-control" name="phone">
</div>

</div>

<div class="row mb-3">

<div class="col">
<label>Position</label>
<select class="form-control" name="position">
<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>
</select>
</div>

<div class="col">
<label>Experience</label>
<input class="form-control" name="experience" placeholder="Years of experience">
</div>

</div>

<div class="mb-3">
<label>Address</label>
<textarea class="form-control" name="address"></textarea>
</div>

<div class="mb-3">
<label>Resume PDF</label>
<input type="file" class="form-control" name="resume">
</div>

<div class="text-center">

<button class="btn btn-success btn-lg px-5">
Submit Application
</button>

</div>

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

    email = request.form["email"]

    conn = get_db()

    exist = conn.execute(
        "SELECT id FROM applicant WHERE email=?",
        (email,)
    ).fetchone()

    if exist:
        return "<h2 style='text-align:center;margin-top:100px;'>You already applied. Please wait for HR.</h2>"

    file = request.files["resume"]
    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    conn.execute("""
    INSERT INTO applicant
    (fullname,nickname,email,phone,position,experience,address,resume)
    VALUES (?,?,?,?,?,?,?,?)
    """,
    (
        request.form["fullname"],
        request.form["nickname"],
        email,
        request.form["phone"],
        request.form["position"],
        request.form["experience"],
        request.form["address"],
        filename
    ))

    conn.commit()
    conn.close()

    return "<h2 style='text-align:center;margin-top:100px;'>Application Submitted</h2>"

# ---------------------
# DASHBOARD
# ---------------------

DASHBOARD_HTML = """

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{background:#f4f6f9;}
.card{
background:white;
border-radius:12px;
box-shadow:0 4px 15px rgba(0,0,0,0.1);
}
</style>

<div class="container mt-5">

<h2 class="text-center mb-4">HR Dashboard</h2>

<div class="card p-3 mb-4 text-center">
<h5>Total Applicants</h5>
<h2>{{total}}</h2>
</div>

<form method="GET" class="mb-3">
<input class="form-control" name="search" placeholder="Search name">
</form>

<div class="card p-4">

<table class="table table-striped">

<thead>
<tr>
<th>ID</th>
<th>Name</th>
<th>Phone</th>
<th>Email</th>
<th>Position</th>
<th>Experience</th>
<th>Address</th>
<th>Resume</th>
<th>Action</th>
</tr>
</thead>

<tbody>

{% for a in applicants %}

<tr>

<td>{{a.id}}</td>

<td>{{a.fullname}} ({{a.nickname}})</td>

<td>{{a.phone}}</td>

<td>{{a.email}}</td>

<td>{{a.position}}</td>

<td>{{a.experience}}</td>

<td>{{a.address}}</td>

<td>

{% if a.resume %}
<a href="/resume/{{a.resume}}" target="_blank" class="btn btn-info btn-sm">View</a>
<a href="/download/{{a.resume}}" class="btn btn-secondary btn-sm">Download</a>
{% endif %}

</td>

<td>
<a href="/delete/{{a.id}}" class="btn btn-danger btn-sm">Delete</a>
</td>

</tr>

{% endfor %}

</tbody>

</table>

<nav>

<ul class="pagination">

{% for p in pages %}

<li class="page-item">
<a class="page-link" href="/dashboard?page={{p}}">{{p}}</a>
</li>

{% endfor %}

</ul>

</nav>

</div>

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
# VIEW RESUME
# ---------------------

@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------------
# DOWNLOAD RESUME
# ---------------------

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)