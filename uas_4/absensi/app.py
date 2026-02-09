from flask import Flask, render_template, request, redirect, session
import sqlite3, uuid, time

app = Flask(__name__)
app.secret_key = "rahasia"

# ========================
# DATABASE
# ========================
def db():
    con = sqlite3.connect("database.db", check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = db()

    con.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT,
        nomor TEXT
    )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS pertemuan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        tanggal TEXT,
        mulai TEXT,
        selesai TEXT
    )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS absensi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomor TEXT,
        pertemuan_id INTEGER,
        UNIQUE(nomor, pertemuan_id)
    )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS token_qr(
        token TEXT,
        nomor TEXT,
        pertemuan_id INTEGER,
        waktu INTEGER
    )
    """)

    con.execute("""
    INSERT OR IGNORE INTO users(username,password,role,nomor)
    VALUES('admin','admin','admin','-')
    """)

    con.commit()


init_db()

# ========================
# ROUTES
# ========================
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        con = db()
        user = con.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        ).fetchone()

        if user:
            session["user"] = dict(user)
            return redirect("/" + user["role"])

    return render_template("login.html")


@app.route("/admin", methods=["GET","POST"])
def admin():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/login")

    con = db()

    if request.method == "POST":
        con.execute(
            "INSERT INTO users(username,password,role,nomor) VALUES(?,?,?,?)",
            (
                request.form["username"],
                request.form["password"],
                request.form["role"],
                request.form["nomor"]
            )
        )
        con.commit()

    if request.args.get("hapus"):
        con.execute("DELETE FROM users WHERE id=?", (request.args["hapus"],))
        con.commit()

    users = con.execute(
        "SELECT id, username, role FROM users WHERE role!='admin'"
    ).fetchall()

    return render_template("admin.html", users=users)


@app.route("/dosen", methods=["GET","POST"])
def dosen():
    con = db()

    if request.method == "POST":
        con.execute(
            "INSERT INTO pertemuan VALUES(NULL,?,?,?,?)",
            (
                request.form["nama"],
                request.form["tanggal"],
                request.form["mulai"],
                request.form["selesai"]
            )
        )
        con.commit()

    data = con.execute("SELECT * FROM pertemuan").fetchall()
    return render_template("dosen.html", pertemuan=data)


@app.route("/detail/<int:id>")
def detail(id):
    con = db()

    p = con.execute(
        "SELECT * FROM pertemuan WHERE id=?",
        (id,)
    ).fetchone()

    hadir = con.execute("""
        SELECT users.username, absensi.nomor
        FROM absensi
        JOIN users ON users.nomor = absensi.nomor
        WHERE absensi.pertemuan_id=?
    """, (id,)).fetchall()

    return render_template("detail_pertemuan.html", p=p, hadir=hadir)


@app.route("/mahasiswa")
def mahasiswa():
    con = db()
    p = con.execute("SELECT * FROM pertemuan").fetchall()
    return render_template("mahasiswa.html", pertemuan=p)


@app.route("/qr/<int:pid>")
def qr(pid):
    nomor = session["user"]["nomor"]
    token = str(uuid.uuid4())

    con = db()
    con.execute(
        "INSERT INTO token_qr VALUES(?,?,?,?)",
        (token, nomor, pid, int(time.time()))
    )
    con.commit()

    return render_template("qr_mahasiswa.html", token=token)


@app.route("/scan/<int:pid>/<token>")
def scan(pid, token):
    con = db()

    t = con.execute(
        "SELECT * FROM token_qr WHERE token=? AND pertemuan_id=?",
        (token, pid)
    ).fetchone()

    if not t:
        return "❌ QR tidak valid"

    try:
        con.execute(
            "INSERT INTO absensi(nomor, pertemuan_id) VALUES(?,?)",
            (t["nomor"], pid)
        )
        con.execute("DELETE FROM token_qr WHERE token=?", (token,))
        con.commit()
        return "✅ Presentasi berhasil"
    except:
        return "❌ Sudah absen sebelumnya"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
