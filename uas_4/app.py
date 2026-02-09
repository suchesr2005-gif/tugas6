from flask import Flask, render_template, request, redirect, session, abort, jsonify
import sqlite3, uuid, qrcode, os

app = Flask(__name__)
app.secret_key = "rahasia"

# ================= DB =================
def db():
    return sqlite3.connect("database.db")

# ================= LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = db().execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()

        if user:
            session["id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect(f"/{user[3]}")

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= ADMIN =================
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        abort(403)

    users = db().execute(
        "SELECT username, role, nomor_induk FROM users"
    ).fetchall()

    return render_template("admin/dashboard.html", users=users)

@app.route("/admin/tambah", methods=["POST"])
def admin_tambah():
    if session.get("role") != "admin":
        abort(403)

    conn = db()
    conn.execute(
        "INSERT INTO users(username,password,role,nomor_induk) VALUES(?,?,?,?)",
        (
            request.form["username"],
            request.form["password"],
            request.form["role"],
            request.form["nomor"]
        )
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

# ================= DOSEN =================
@app.route("/dosen")
def dosen():
    if session.get("role") != "dosen":
        abort(403)
    return render_template("dosen/dashboard.html")

@app.route("/dosen/pertemuan", methods=["GET","POST"])
def dosen_pertemuan():
    if session.get("role") != "dosen":
        abort(403)

    conn = db()

    if request.method == "POST":
        conn.execute("""
            INSERT INTO pertemuan(nama,tanggal,jam_masuk,jam_keluar,dosen_id)
            VALUES(?,?,?,?,?)
        """,(
            request.form["nama"],
            request.form["tanggal"],
            request.form["masuk"],
            request.form["keluar"],
            session["id"]
        ))
        conn.commit()

    data = conn.execute(
        "SELECT * FROM pertemuan WHERE dosen_id=?",
        (session["id"],)
    ).fetchall()

    conn.close()
    return render_template("dosen/pertemuan.html", data=data)

@app.route("/dosen/pertemuan/<int:id>")
def dosen_detail(id):
    if session.get("role") != "dosen":
        abort(403)

    conn = db()
    p = conn.execute("SELECT * FROM pertemuan WHERE id=?", (id,)).fetchone()

    hadir = conn.execute("""
        SELECT u.username, u.nomor_induk
        FROM absensi a JOIN users u ON a.mahasiswa_id = u.id
        WHERE a.pertemuan_id=?
    """, (id,)).fetchall()

    # Pastikan ini hanya mengambil token jika 'aktif=1'
    qr = conn.execute("""
        SELECT * FROM qr_token 
        WHERE pertemuan_id=? AND aktif=1 
        LIMIT 1
    """, (id,)).fetchone()

    conn.close()
    return render_template("dosen/detail_pertemuan.html", pertemuan=p, hadir=hadir, qr=qr)
# Tambahkan "json" dan "jsonify" pada import di baris paling atas
# dari flask import Flask, ..., request, jsonify
@app.route("/dosen/pertemuan/<int:id>/start", methods=["POST"])
def mulai_presentasi(id):
    if session.get("role") != "dosen":
        abort(403)

    conn = db()

    # matikan QR lama
    conn.execute(
        "UPDATE qr_token SET aktif=0 WHERE pertemuan_id=?",
        (id,)
    )

    # buat token baru
    token = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO qr_token(pertemuan_id, token, aktif)
        VALUES(?,?,1)
    """, (id, token))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


@app.route("/dosen/proses_absen", methods=["POST"])
def proses_absen():
    if session.get("role") != "dosen":
        return jsonify({"status": "error", "message": "Akses ditolak"}), 403

    data = request.json
    nomor_induk = data.get("nomor_induk")
    pertemuan_id = data.get("pertemuan_id")

    conn = db()

    mhs = conn.execute(
        "SELECT id FROM users WHERE nomor_induk=?",
        (nomor_induk,)
    ).fetchone()

    if not mhs:
        conn.close()
        return jsonify({"status": "error", "message": "Mahasiswa tidak terdaftar"})

    cek = conn.execute("""
        SELECT * FROM absensi
        WHERE pertemuan_id=? AND mahasiswa_id=?
    """, (pertemuan_id, mhs[0])).fetchone()

    if cek:
        conn.close()
        return jsonify({"status": "error", "message": "Sudah absen"})

    conn.execute("""
        INSERT INTO absensi(pertemuan_id, mahasiswa_id)
        VALUES(?,?)
    """, (pertemuan_id, mhs[0]))

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Berhasil absen"})

@app.route("/mahasiswa/pertemuan/<int:id>")
def mhs_detail(id):
    if session.get("role") != "mahasiswa":
        abort(403)

    conn = db()

    p = conn.execute(
        "SELECT * FROM pertemuan WHERE id=?",
        (id,)
    ).fetchone()

    qr = conn.execute("""
        SELECT * FROM qr_token
        WHERE pertemuan_id=? AND aktif=1
    """,(id,)).fetchone()

    conn.close()

    return render_template(
        "mahasiswa/detail_pertemuan.html",
        pertemuan=p, qr=qr
    )

@app.route("/mahasiswa/scan/<token>")
def scan(token):
    if session.get("role") != "mahasiswa":
        abort(403)
    return render_template("mahasiswa/scan.html", token=token)

@app.route("/hadir/<token>")
def hadir(token):
    if session.get("role") != "mahasiswa":
        abort(403)

    conn = db()

    qr = conn.execute(
        "SELECT * FROM qr_token WHERE token=? AND aktif=1",
        (token,)
    ).fetchone()

    if not qr:
        conn.close()
        return "QR tidak valid"

    cek = conn.execute("""
        SELECT * FROM absensi
        WHERE pertemuan_id=? AND mahasiswa_id=?
    """,(qr[1], session["id"])).fetchone()

    if cek:
        conn.close()
        return "Mahasiswa sudah presentasi"

    conn.execute("""
        INSERT INTO absensi(pertemuan_id,mahasiswa_id)
        VALUES(?,?)
    """,(qr[1], session["id"]))

    conn.commit()
    conn.close()

    return "Presensi berhasil"

# ================= FORBIDDEN =================
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
