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
# NAVBAR TEMPLATE
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

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<meta name="viewport" content="width=device-width, initial-scale=1">

"""


# ---------------------
# HOME
# ---------------------

@app.route("/")
def home():

    html = NAVBAR + """

<div class="container mt-5">

<div class="text-center">

<h1>Welcome to Our Company</h1>

<p class="lead">
Innovative technology solutions for the modern world
</p>

<a href="/jobs" class="btn btn-primary btn-lg mt-3">
Apply for Job
</a>

</div>

</div>

"""

    return render_template_string(html)


# ---------------------
# ABOUT US
# ---------------------

@app.route("/about")
def about():

    html = NAVBAR + """

<div class="container mt-5">

<h2>About Our Company</h2>

<p>
We are a technology company focused on building innovative software
solutions for businesses worldwide.
</p>

<p>
Our mission is to create powerful digital platforms that help companies
grow and succeed in the digital age.
</p>

</div>

"""

    return render_template_string(html)


# ---------------------
# CONTACT
# ---------------------

@app.route("/contact")
def contact():

    html = NAVBAR + """

<div class="container mt-5">

<h2 class="mb-4">Contact Us</h2>

<div class="row">

<div class="col-md-6">

<p><b>Email:</b> hr@company.com</p>
<p><b>Phone:</b> +66 000 000 000</p>
<p><b>Address:</b> Bangkok, Thailand</p>

</div>

<div class="col-md-6">

<iframe
width="100%"
height="300"
style="border:0"
loading="lazy"
allowfullscreen
src="https://www.google.com/maps?q=Yada Building, Bangkok, Thailand&output=embed">

</div>

</div>

</div>

"""

    return render_template_string(html)


# ---------------------
# JOB APPLICATION PAGE
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

<select class="form-control" name="position" required>
<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>
</select>

</div>

<div class="col-md-6">

<label>Experience</label>

<input class="form-control" name="experience" required>

</div>

</div>

<div class="mb-3">

<label>Address</label>

<textarea class="form-control" name="address" required></textarea>

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

    fullname = request.form["fullname"]
    nickname = request.form["nickname"]
    age = request.form["age"]
    email = request.form["email"]
    phone = request.form["phone"]
    position = request.form["position"]
    experience = request.form["experience"]
    address = request.form["address"]

    file = request.files["resume"]

    filename = str(uuid.uuid4()) + ".pdf"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = get_db()

    conn.execute("""
    INSERT INTO applicant
    (fullname,nickname,age,email,phone,position,experience,address,resume)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (fullname,nickname,age,email,phone,position,experience,address,filename))

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

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<div class="container mt-5" style="max-width:400px">

<h3 class="text-center">Admin Login</h3>

<form method="POST">

<input class="form-control mb-3" name="user" placeholder="Username">

<input class="form-control mb-3" name="pw" type="password" placeholder="Password">

<button class="btn btn-primary w-100">Login</button>

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

    conn = get_db()

    data = conn.execute("SELECT * FROM applicant").fetchall()

    conn.close()

    html = NAVBAR + """   

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<div class="container mt-5">

<h2>HR Dashboard</h2>

<table class="table table-striped">

<tr>
<th>ID</th>
<th>Name</th>
<th>Age</th>
<th>Email</th>
<th>Position</th>
<th>Resume</th>
<th>Action</th>
</tr>

"""

    for a in data:

        html += f"""

<tr>
<td>{a['id']}</td>
<td>{a['fullname']}</td>
<td>{a['age']}</td>
<td>{a['email']}</td>
<td>{a['position']}</td>
<td><a href="/resume/{a['resume']}">View</a></td>
<td><a href="/delete/{a['id']}" class="btn btn-danger btn-sm">Delete</a></td>
</tr>

"""

    html += "</table></div>"

    return html


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)