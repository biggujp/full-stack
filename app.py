from flask import Flask, request, redirect, render_template_string, session, send_from_directory
import sqlite3
import os
import uuid

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
        age INTEGER,
        email TEXT UNIQUE,
        phone TEXT,
        position TEXT,
        experience TEXT,
        address TEXT,
        resume TEXT,
        status TEXT DEFAULT 'New'
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------------
# NAVBAR
# ---------------------

NAVBAR = """

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">

<div class="container">

<a class="navbar-brand" href="/">Tiger J Co., Ltd.</a>

<button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#menu">
<span class="navbar-toggler-icon"></span>
</button>

<div class="collapse navbar-collapse" id="menu">

<ul class="navbar-nav ms-auto">

<li class="nav-item">
<a class="nav-link" href="/">HOME</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/jobs">JOB APPLICATION</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/login">ADMIN</a>
</li>

</ul>

</div>

</div>

</nav>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

"""


# ---------------------
# HOME
# ---------------------

@app.route("/")
def home():

    html = NAVBAR + """

<div class="container mt-5 text-center">

<h1>Welcome to Tiger J Co., Ltd.</h1>

<p class="lead">
Join our team and build amazing technology with us
</p>

<a href="/jobs" class="btn btn-primary btn-lg">
Apply for Job
</a>

</div>

"""

    return render_template_string(html)


# ---------------------
# JOB APPLICATION
# ---------------------

@app.route("/jobs")
def jobs():

    html = NAVBAR + """

<div class="container mt-5">

<h2 class="mb-4">Job Application</h2>

<div class="card p-4 shadow">

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

<select class="form-control" name="position">
<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>
</select>

</div>

<div class="col-md-6">
<label>Experience</label>
<input class="form-control" name="experience">
</div>

</div>


<div class="mb-3">

<label>Address</label>

<textarea class="form-control" name="address"></textarea>

</div>


<div class="mb-3">

<label>Resume (PDF)</label>

<input type="file" class="form-control" name="resume" required>

</div>


<button class="btn btn-success w-100 btn-lg">
Submit Application
</button>

</form>

</div>

</div>

"""

    return render_template_string(html)


# ---------------------
# APPLY
# ---------------------

@app.route("/apply", methods=["POST"])
def apply():

    file = request.files["resume"]

    filename = str(uuid.uuid4()) + ".pdf"

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = get_db()

    conn.execute("""

    INSERT INTO applicant
    (fullname,nickname,age,email,phone,position,experience,address,resume)

    VALUES (?,?,?,?,?,?,?,?,?)

    """,

    (
    request.form["fullname"],
    request.form["nickname"],
    request.form["age"],
    request.form["email"],
    request.form["phone"],
    request.form["position"],
    request.form["experience"],
    request.form["address"],
    filename
    )

    )

    conn.commit()
    conn.close()

    return redirect("/jobs")


# ---------------------
# LOGIN
# ---------------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["user"] == "admin" and request.form["pw"] == "1234":

            session["login"] = True
            return redirect("/dashboard")

    html = NAVBAR + """

<div class="container mt-5" style="max-width:400px">

<h3 class="text-center">Admin Login</h3>

<form method="POST">

<input class="form-control mb-3" name="user" placeholder="Username">

<input class="form-control mb-3" name="pw" type="password" placeholder="Password">

<button class="btn btn-primary w-100">
Login
</button>

</form>

</div>

"""

    return render_template_string(html)


# ---------------------
# DASHBOARD
# ---------------------

@app.route("/dashboard")
def dashboard():

    if not session.get("login"):
        return redirect("/login")

    page = request.args.get("page",1,type=int)
    search = request.args.get("search","")

    offset = (page-1)*PER_PAGE

    conn = get_db()

    if search:

        data = conn.execute("""

        SELECT * FROM applicant
        WHERE fullname LIKE ?
        OR email LIKE ?
        OR position LIKE ?
        LIMIT ? OFFSET ?

        """,

        (f"%{search}%",f"%{search}%",f"%{search}%",PER_PAGE,offset)

        ).fetchall()

        total = conn.execute("""

        SELECT COUNT(*) FROM applicant
        WHERE fullname LIKE ?
        OR email LIKE ?
        OR position LIKE ?

        """,

        (f"%{search}%",f"%{search}%",f"%{search}%")

        ).fetchone()[0]

    else:

        data = conn.execute(

        "SELECT * FROM applicant LIMIT ? OFFSET ?",

        (PER_PAGE,offset)

        ).fetchall()

        total = conn.execute(
        "SELECT COUNT(*) FROM applicant"
        ).fetchone()[0]


    stats = conn.execute("""

    SELECT position,COUNT(*) as total
    FROM applicant
    GROUP BY position

    """).fetchall()

    conn.close()

    pages = total//PER_PAGE + (1 if total%PER_PAGE else 0)

    html = NAVBAR + f"""

<div class="container mt-5">

<h2 class="mb-4">HR Dashboard</h2>

<form class="mb-3">
<input class="form-control" name="search" placeholder="Search Applicant" value="{search}">
</form>


<div class="row mb-4">

<div class="col-md-3">

<div class="card text-center p-3">

<h5>Total Applicants</h5>

<h3>{total}</h3>

</div>

</div>

"""

    for s in stats:

        html += f"""

<div class="col-md-3">

<div class="card text-center p-3">

<h6>{s['position']}</h6>

<h4>{s['total']}</h4>

</div>

</div>

"""

    html += """

</div>


<div class="table-responsive">

<table class="table table-bordered table-hover">

<tr>
<th>ID</th>
<th>Name</th>
<th>Email</th>
<th>Phone</th>
<th>Position</th>
<th>Status</th>
<th>Resume</th>
<th>Action</th>
</tr>

"""

    for a in data:

        html += f"""

<tr>

<td>{a['id']}</td>

<td>
<b>{a['fullname']}</b><br>
<small>{a['nickname']}</small>
</td>

<td>{a['email']}</td>
<td>{a['phone']}</td>
<td>{a['position']}</td>

<td>
<span class="badge bg-info">
{a['status']}
</span>
</td>

<td>

<a class="btn btn-sm btn-primary"
href="/resume/{a['resume']}"
target="_blank">
View
</a>

<a class="btn btn-sm btn-success"
href="/download/{a['resume']}">
Download
</a>

</td>

<td>

<a class="btn btn-sm btn-danger"
href="/delete/{a['id']}">
Delete
</a>

</td>

</tr>

"""

    html += "</table></div><ul class='pagination'>"

    for p in range(1,pages+1):

        html += f"""

<li class="page-item">

<a class="page-link"
href="/dashboard?page={p}&search={search}">

{p}

</a>

</li>

"""

    html += "</ul></div>"

    return html


# ---------------------
# DELETE
# ---------------------

@app.route("/delete/<id>")
def delete(id):

    conn = get_db()

    conn.execute(
    "DELETE FROM applicant WHERE id=?",
    (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------------
# RESUME VIEW
# ---------------------

@app.route("/resume/<filename>")
def resume(filename):

    return send_from_directory(
    UPLOAD_FOLDER,
    filename
    )


# ---------------------
# DOWNLOAD RESUME
# ---------------------

@app.route("/download/<filename>")
def download(filename):

    return send_from_directory(
    UPLOAD_FOLDER,
    filename,
    as_attachment=True
    )


# ---------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)