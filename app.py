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

    conn.execute("""
    CREATE TABLE IF NOT EXISTS job_post(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS news(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
<a class="nav-link" href="/about">ABOUT US</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/jobs">JOB APPLICATION</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/contact">CONTACT US</a>
</li>

<li class="nav-item">
<a class="nav-link" href="/login">ADMIN</a>
</li>

</ul>

</div>

</div>

</nav>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

"""


# ---------------------
# HOME
# ---------------------

@app.route("/")
def home():

    conn = get_db()

    news = conn.execute(
        "SELECT * FROM news ORDER BY id DESC LIMIT 5"
    ).fetchall()

    jobs = conn.execute(
        "SELECT * FROM job_post ORDER BY id DESC LIMIT 5"
    ).fetchall()

    conn.close()

    html = NAVBAR + """

<div class="container mt-5 text-center">

<h1>Welcome to Tiger J Co., Ltd.</h1>

<p class="lead">
Join our team and build amazing technology with us
</p>

</div>

<div class="container mt-5">

<h3 class="mb-4">Company News</h3>

"""

    for n in news:

        html += f"""
        <div class="card p-3 mb-3 shadow-sm">
        <h5>{n['title']}</h5>
        <p>{n['content']}</p>
        </div>
        """

    html += """

<h3 class="mt-5 mb-4">Job Announcements</h3>

"""

    for j in jobs:

        html += f"""
        <div class="card p-3 mb-3 shadow-sm">
        <h5>{j['title']}</h5>
        <p>{j['description']}</p>
        </div>
        """

    html += "</div>"

    return html


# ---------------------
# ABOUT
# ---------------------

@app.route("/about")
def about():

    html = NAVBAR + """

<div class="container mt-5">

<h2>About Our Company</h2>

<p>
We are a technology company focused on building innovative software solutions.
</p>

</div>

"""

    return html


# ---------------------
# CONTACT
# ---------------------

@app.route("/contact")
def contact():

    html = NAVBAR + """

<div class="container mt-5">

<h2>Contact Us</h2>

<p>Email: hr.tigerj@gmail.com</p>

<p>Phone: 02-266-4902</p>

</div>

"""

    return html


# ---------------------
# JOB APPLICATION FORM
# ---------------------

@app.route("/jobs")
def jobs():

    html = NAVBAR + """

<div class="container mt-5">

<h2 class="mb-4">Job Application</h2>

<div class="card p-4 shadow">

<form method="POST" action="/apply" enctype="multipart/form-data">

<input class="form-control mb-2" name="fullname" placeholder="Full Name" required>
<input class="form-control mb-2" name="nickname" placeholder="Nickname">
<input class="form-control mb-2" name="age" type="number" placeholder="Age">
<input class="form-control mb-2" name="email" placeholder="Email">
<input class="form-control mb-2" name="phone" placeholder="Phone">

<select class="form-control mb-2" name="position">
<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>
</select>

<input class="form-control mb-2" name="experience" placeholder="Experience">

<textarea class="form-control mb-2" name="address" placeholder="Address"></textarea>

<input type="file" class="form-control mb-3" name="resume">

<button class="btn btn-success w-100">
Submit Application
</button>

</form>

</div>

</div>

"""

    return html


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
    ))

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

<h3>Admin Login</h3>

<form method="POST">

<input class="form-control mb-3" name="user" placeholder="Username">

<input class="form-control mb-3" name="pw" type="password" placeholder="Password">

<button class="btn btn-primary w-100">
Login
</button>

</form>

</div>

"""

    return html


# ---------------------
# DASHBOARD
# ---------------------

@app.route("/dashboard")
def dashboard():

    if not session.get("login"):
        return redirect("/login")

    conn = get_db()

    applicants = conn.execute(
        "SELECT * FROM applicant ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = NAVBAR + """

<div class="container mt-5">

<h2 class="mb-4">HR Dashboard</h2>

<a class="btn btn-success mb-3" href="/manage_jobs">
Manage Job Posts
</a>

<a class="btn btn-warning mb-3" href="/manage_news">
Manage News
</a>

<div class="table-responsive">

<table class="table table-bordered table-hover">

<tr>
<th>ID</th>
<th>Name</th>
<th>Nickname</th>
<th>Age</th>
<th>Email</th>
<th>Phone</th>
<th>Position</th>
<th>Experience</th>
<th>Address</th>
<th>Status</th>
<th>Resume</th>
<th>Action</th>
</tr>

"""

    for a in applicants:

        html += f"""

<tr>

<td>{a['id']}</td>

<td>{a['fullname']}</td>

<td>{a['nickname']}</td>

<td>{a['age']}</td>

<td>{a['email']}</td>

<td>{a['phone']}</td>

<td>{a['position']}</td>

<td>{a['experience']}</td>

<td>{a['address']}</td>

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

    html += """

</table>

</div>

</div>

"""

    return html


# ---------------------
# DELETE APPLICANT
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
# MANAGE JOB POSTS
# ---------------------

@app.route("/manage_jobs", methods=["GET","POST"])
def manage_jobs():

    if not session.get("login"):
        return redirect("/login")

    conn = get_db()

    if request.method == "POST":

        conn.execute(
            "INSERT INTO job_post (title,description) VALUES (?,?)",
            (
                request.form["title"],
                request.form["description"]
            )
        )

        conn.commit()

    jobs = conn.execute(
        "SELECT * FROM job_post ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = NAVBAR + """

<div class="container mt-5">

<h3>Manage Job Announcements</h3>

<form method="POST" class="mb-4">

<input class="form-control mb-2" name="title" placeholder="Job Title">

<textarea class="form-control mb-2" name="description" placeholder="Description"></textarea>

<button class="btn btn-success">
Add Job
</button>

</form>

<table class="table">

<tr>
<th>ID</th>
<th>Title</th>
<th>Action</th>
</tr>

"""

    for j in jobs:

        html += f"""

<tr>

<td>{j['id']}</td>

<td>{j['title']}</td>

<td>

<a class="btn btn-danger btn-sm"
href="/delete_job/{j['id']}">
Delete
</a>

</td>

</tr>

"""

    html += "</table></div>"

    return html


# ---------------------
# DELETE JOB
# ---------------------

@app.route("/delete_job/<id>")
def delete_job(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM job_post WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_jobs")


# ---------------------
# MANAGE NEWS
# ---------------------

@app.route("/manage_news", methods=["GET","POST"])
def manage_news():

    if not session.get("login"):
        return redirect("/login")

    conn = get_db()

    if request.method == "POST":

        conn.execute(
            "INSERT INTO news (title,content) VALUES (?,?)",
            (
                request.form["title"],
                request.form["content"]
            )
        )

        conn.commit()

    news = conn.execute(
        "SELECT * FROM news ORDER BY id DESC"
    ).fetchall()

    conn.close()

    html = NAVBAR + """

<div class="container mt-5">

<h3>Manage Company News</h3>

<form method="POST" class="mb-4">

<input class="form-control mb-2" name="title" placeholder="News Title">

<textarea class="form-control mb-2" name="content" placeholder="Content"></textarea>

<button class="btn btn-warning">
Add News
</button>

</form>

<table class="table">

<tr>
<th>ID</th>
<th>Title</th>
<th>Action</th>
</tr>

"""

    for n in news:

        html += f"""

<tr>

<td>{n['id']}</td>

<td>{n['title']}</td>

<td>

<a class="btn btn-danger btn-sm"
href="/delete_news/{n['id']}">
Delete
</a>

</td>

</tr>

"""

    html += "</table></div>"

    return html


# ---------------------
# DELETE NEWS
# ---------------------

@app.route("/delete_news/<id>")
def delete_news(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM news WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_news")


# ---------------------
# RESUME VIEW
# ---------------------

@app.route("/resume/<filename>")
def resume(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

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