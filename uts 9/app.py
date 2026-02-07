from flask import Flask, render_template, request, redirect, session, abort
import sqlite3

app = Flask(__name__)
app.secret_key = "rahasia_flask"

# =========================
# DATABASE
# =========================
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================
# HOME + BUAT AKUN + LIST
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        try:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?,?,?)",
                (username, password, role)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            error = "Username sudah digunakan!"

    users = conn.execute(
        "SELECT id, username, role FROM users"
    ).fetchall()
    conn.close()

    return render_template("home.html", users=users, error=error)

# =========================
# HAPUS AKUN
# =========================
@app.route("/delete/<int:id>")
def delete_user(id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    # jika sudah login, lempar ke dashboard sesuai role
    if "user" in session:
        role = session.get("role")
        if role == "mahasiswa":
            return redirect("/mahasiswa")
        elif role == "dosen":
            return redirect("/dosen")
        elif role == "admin":
            return redirect("/admin")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "mahasiswa":
                return redirect("/mahasiswa")
            elif user["role"] == "dosen":
                return redirect("/dosen")
            elif user["role"] == "admin":
                return redirect("/admin")

        return "Login gagal"

    return render_template("login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/mahasiswa")
def mahasiswa():
    if "user" not in session:
        return redirect("/login")
    if session.get("role") != "mahasiswa":
        abort(403)
    return render_template("mahasiswa.html")

@app.route("/dosen")
def dosen():
    if "user" not in session:
        return redirect("/login")
    if session.get("role") != "dosen":
        abort(403)
    return render_template("dosen.html")

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        abort(403)
    return render_template("admin.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================
# ERROR 403
# =========================
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
