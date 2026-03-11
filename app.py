from flask import Flask, request, redirect, render_template_string, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "hrsystem"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------
# DATABASE
# -------------------

def get_db():
    conn = sqlite3.connect("job_hr.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS applicant(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        position TEXT,
        experience INTEGER,
        resume TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------
# LOGIN
# -------------------

LOGIN = """

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{
background:#121212;
color:white;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}
.card{
background:#1e1e1e;
padding:40px;
width:350px;
}
</style>

<div class="card">

<h3 class="mb-3">HR Login</h3>

<form method="POST">

<input class="form-control mb-3" name="user" placeholder="Username">
<input class="form-control mb-3" name="pw" type="password" placeholder="Password">

<button class="btn btn-success w-100">Login</button>

</form>

</div>
"""

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["user"] == "admin" and request.form["pw"] == "1234":

            session["login"] = True
            return redirect("/")

    return render_template_string(LOGIN)

# -------------------
# MAIN PAGE
# -------------------

INDEX_HTML = """

<!DOCTYPE html>
<html>
<head>

<title>Job Application Form</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:#121212;
color:white;
}

.card{
background:#1e1e1e;
border:none;
}

input,select,textarea{
background:#2b2b2b !important;
color:white !important;
border:none !important;
}

</style>

</head>

<body>

<div class="container mt-5">

<h2 class="text-center mb-4">Job Application Form</h2>

<div class="card p-4">

<form method="POST" action="/apply" enctype="multipart/form-data">

<div class="row mb-3">

<div class="col">
<label>First Name</label>
<input class="form-control" name="firstname" required>
</div>

<div class="col">
<label>Last Name</label>
<input class="form-control" name="lastname" required>
</div>

</div>

<div class="row mb-3">

<div class="col">
<label>Email</label>
<input class="form-control" name="email" type="email" required>
</div>

<div class="col">
<label>Phone</label>
<input class="form-control" name="phone">
</div>

</div>

<div class="row mb-3">

<div class="col">
<label>Position Applied</label>
<select class="form-control" name="position">

<option>Software Developer</option>
<option>Data Analyst</option>
<option>UX Designer</option>
<option>Marketing</option>

</select>
</div>

<div class="col">
<label>Years of Experience</label>
<input class="form-control" name="experience">
</div>

</div>

<div class="mb-3">

<label>Address</label>
<textarea class="form-control" name="address"></textarea>

</div>

<div class="mb-3">

<label>Upload Resume (PDF)</label>
<input type="file" class="form-control" name="resume">

</div>

<div class="text-center">

<button class="btn btn-success btn-lg">
Submit Application
</button>

</div>

</form>

</div>

</div>

</body>

</html>

"""


HTML = """

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:#121212;
color:white;
}

.card{
background:#1e1e1e;
border:none;
}

input{
background:#2b2b2b !important;
color:white !important;
border:none !important;
}

table{
color:white;
}

</style>

<div class="container mt-5">

<h2 class="text-center mb-4">HR Dashboard</h2>

<div class="row mb-4 text-center">

<div class="col">
<div class="card p-3">
<h5>Total Applicants</h5>
<h2>{{total}}</h2>
</div>
</div>

</div>

<div class="card p-4 mb-4">

<form method="POST" action="/add" enctype="multipart/form-data">

<div class="row">

<div class="col">
<input class="form-control" name="name" placeholder="Name">
</div>

<div class="col">
<input class="form-control" name="email" placeholder="Email">
</div>

<div class="col">
<input class="form-control" name="position" placeholder="Position">
</div>

<div class="col">
<input class="form-control" name="experience" placeholder="Experience">
</div>

<div class="col">
<input type="file" class="form-control" name="resume">
</div>

<div class="col">
<button class="btn btn-success">Add</button>
</div>

</div>

</form>

</div>

<div class="card p-4 mb-4">

<form method="GET">

<div class="row">

<div class="col">
<input class="form-control" name="search" placeholder="Search name">
</div>

<div class="col">
<button class="btn btn-primary">Search</button>
</div>

</div>

</form>

</div>

<div class="card p-4">

<table class="table table-dark table-striped">

<thead>

<tr>
<th>ID</th>
<th>Name</th>
<th>Email</th>
<th>Position</th>
<th>Exp</th>
<th>Resume</th>
<th>Action</th>
</tr>

</thead>

<tbody>

{% for a in applicants %}

<tr>

<td>{{a.id}}</td>
<td>{{a.name}}</td>
<td>{{a.email}}</td>
<td>{{a.position}}</td>
<td>{{a.experience}}</td>

<td>

{% if a.resume %}
<a href="/resume/{{a.resume}}" target="_blank" class="btn btn-info btn-sm">
View
</a>
{% endif %}

</td>

<td>

<a href="/edit/{{a.id}}" class="btn btn-warning btn-sm">
Edit
</a>

<a href="/delete/{{a.id}}" class="btn btn-danger btn-sm">
Delete
</a>

</td>

</tr>

{% endfor %}

</tbody>

</table>

</div>

</div>
"""

# -------------------
# HOME
# -------------------

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/apply", methods=["POST"])
def apply():

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    phone = request.form["phone"]
    position = request.form["position"]
    experience = request.form["experience"]
    address = request.form["address"]

    file = request.files["resume"]

    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join("uploads", filename))

    conn = get_db()

    conn.execute("""
    INSERT INTO applicant
    (name,email,position,experience,resume)
    VALUES (?,?,?,?,?)
    """,
    (firstname+" "+lastname,email,position,experience,filename))

    conn.commit()
    conn.close()

    return "<h2 style='text-align:center;margin-top:100px;'>Application Submitted Successfully</h2>"


@app.route("/admin")
def admin():

    if not session.get("login"):
        return redirect("/login")

    search = request.args.get("search")

    conn = get_db()

    if search:
        applicants = conn.execute(
            "SELECT * FROM applicant WHERE name LIKE ?",
            ('%'+search+'%',)
        ).fetchall()
    else:
        applicants = conn.execute(
            "SELECT * FROM applicant"
        ).fetchall()

    total = conn.execute("SELECT COUNT(*) FROM applicant").fetchone()[0]

    conn.close()

    return render_template_string(HTML, applicants=applicants, total=total)

# -------------------
# ADD
# -------------------

@app.route("/add", methods=["POST"])
def add():

    file = request.files["resume"]

    filename = ""

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    conn = get_db()

    conn.execute(
        "INSERT INTO applicant(name,email,position,experience,resume) VALUES (?,?,?,?,?)",
        (
            request.form["name"],
            request.form["email"],
            request.form["position"],
            request.form["experience"],
            filename
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")

# -------------------
# DELETE
# -------------------

@app.route("/delete/<id>")
def delete(id):

    conn = get_db()

    conn.execute("DELETE FROM applicant WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/")

# -------------------
# EDIT
# -------------------

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):

    conn = get_db()

    if request.method == "POST":

        conn.execute("""
        UPDATE applicant
        SET name=?,email=?,position=?,experience=?
        WHERE id=?
        """,
        (
            request.form["name"],
            request.form["email"],
            request.form["position"],
            request.form["experience"],
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    applicant = conn.execute(
        "SELECT * FROM applicant WHERE id=?",(id,)
    ).fetchone()

    conn.close()

    return f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class='container mt-5'>
    <h3>Edit Applicant</h3>
    <form method='POST'>
    <input class='form-control mb-2' name='name' value='{applicant["name"]}'>
    <input class='form-control mb-2' name='email' value='{applicant["email"]}'>
    <input class='form-control mb-2' name='position' value='{applicant["position"]}'>
    <input class='form-control mb-2' name='experience' value='{applicant["experience"]}'>
    <button class='btn btn-warning'>Update</button>
    </form>
    </div>
    """

# -------------------
# VIEW RESUME
# -------------------

@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory("uploads", filename)

# -------------------

if __name__ == "__main__":
    app.run(debug=True)