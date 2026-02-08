from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ===================== DATABASE =====================

def db():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con

# ===================== HELPER =====================

def load_ortu(con):
    rows = con.execute("SELECT * FROM ortu").fetchall()
    return {r["anak_id"]: (r["ayah"], r["ibu"]) for r in rows}

def saudara_kandung(id, ortu):
    if id not in ortu:
        return []
    ay, ib = ortu[id]
    return [
        a for a, (x, y) in ortu.items()
        if a != id and x == ay and y == ib
    ]

def sepupu(id, level, ortu):
    if id not in ortu:
        return []

    ay, ib = ortu[id]
    if not ay or not ib:
        return []

    paman_bibi = saudara_kandung(ay, ortu) + saudara_kandung(ib, ortu)
    current = set(paman_bibi)

    for _ in range(level - 1):
        next_set = set()
        for p in current:
            next_set.update(saudara_kandung(p, ortu))
        current = next_set

    hasil = set()
    for anak_id, (a, b) in ortu.items():
        if a in current or b in current:
            hasil.add(anak_id)
    return list(hasil)

# ===================== ROUTE UTAMA =====================

@app.route("/")
def index():
    con = db()
    q = request.args.get("q", "").strip()

    if q:
        orang = con.execute(
            "SELECT * FROM orang WHERE nama LIKE ? ORDER BY nama",
            (f"%{q}%",)
        ).fetchall()
    else:
        orang = con.execute(
            "SELECT * FROM orang ORDER BY nama"
        ).fetchall()

    return render_template("index.html", orang=orang, q=q)

@app.route("/orang/<int:id>")
def detail(id):
    con = db()
    orang = con.execute("SELECT * FROM orang WHERE id=?", (id,)).fetchone()

    ortu = con.execute("""
        SELECT o.*
        FROM ortu t
        JOIN orang o ON o.id=t.ayah OR o.id=t.ibu
        WHERE t.anak_id=?
    """, (id,)).fetchall()

    anak = con.execute("""
        SELECT o.*
        FROM ortu t
        JOIN orang o ON o.id=t.anak_id
        WHERE t.ayah=? OR t.ibu=?
    """, (id, id)).fetchall()

    saudara = con.execute("""
        SELECT o.*
        FROM ortu a
        JOIN ortu b ON a.ayah=b.ayah AND a.ibu=b.ibu
        JOIN orang o ON o.id=b.anak_id
        WHERE a.anak_id=? AND b.anak_id!=?
    """, (id, id)).fetchall()

    pasangan = con.execute("""
        SELECT o.id, o.nama
        FROM nikah n
        JOIN orang o
          ON (o.id = n.istri AND n.suami = ?)
          OR (o.id = n.suami AND n.istri = ?)
    """, (id, id)).fetchall()

    return render_template(
        "detail.html",
        orang=orang,
        ortu=ortu,
        anak=anak,
        saudara=saudara,
        pasangan=pasangan
    )

# ===================== SEPUPU =====================

# Masukkan ini di bagian ===================== HELPER =====================
def get_sepupu(id, level, ortu_map):
    if id not in ortu_map or level < 1:
        return []

    # Ambil data orang tua
    ay, ib = ortu_map[id]
    
    # Kumpulkan semua orang yang HARUS DIABAIKAN (Diri sendiri + Saudara Kandung)
    ignored = {id}
    ignored.update(saudara_kandung(id, ortu_map))

    # Tentukan leluhur awal (paman/bibi adalah saudara kandung orang tua)
    # Ini adalah "ancestor branch" untuk sepupu level 1
    current_ancestors = set(saudara_kandung(ay, ortu_map) + saudara_kandung(ib, ortu_map))
    
    # Jika level > 1, kita harus naik ke atas (kakek, buyut, dst)
    # Sambil mencatat sepupu level di bawahnya untuk diabaikan
    for i in range(1, level):
        # Tambahkan semua anak dari leluhur saat ini ke daftar ignore
        # (Karena mereka adalah sepupu level yang lebih rendah)
        for anak_id, (a, b) in ortu_map.items():
            if a in current_ancestors or b in current_ancestors:
                ignored.add(anak_id)
        
        # Naik satu tingkat ke saudara dari orang tua leluhur saat ini
        next_ancestors = set()
        for anc_id in current_ancestors:
            if anc_id in ortu_map:
                par_a, par_b = ortu_map[anc_id]
                next_ancestors.update(saudara_kandung(par_a, ortu_map))
                next_ancestors.update(saudara_kandung(par_b, ortu_map))
        current_ancestors = next_ancestors

    # Ambil anak-anak dari leluhur di level target yang tidak ada di daftar ignore
    hasil = []
    for anak_id, (a, b) in ortu_map.items():
        if (a in current_ancestors or b in current_ancestors) and anak_id not in ignored:
            hasil.append(anak_id)
            
    return hasil

# ===================== ROUTE UTAMA =====================
@app.route("/orang/<int:id>/sepupu/<int:level>")
def sepupu_view(id, level):
    con = db()
    orang = con.execute("SELECT * FROM orang WHERE id=?", (id,)).fetchone()
    if not orang:
        return "Orang tidak ditemukan", 404

    ortu_map = load_ortu(con)
    
    # Panggil fungsi helper yang sudah diperbaiki
    ids = get_sepupu(id, level, ortu_map)

    data = []
    for sid in ids:
        o = con.execute("SELECT * FROM orang WHERE id=?", (sid,)).fetchone()
        if o:
            data.append(o)

    return render_template("sepupu.html", orang=orang, sepupu=data, level=level)
# ===================== TAMBAH DATA =====================

@app.route("/tambah")
def tambah():
    return render_template("tambah_data.html")

@app.route("/tambah/orang", methods=["GET", "POST"])
def tambah_orang():
    if request.method == "POST":
        con = db()
        con.execute(
            "INSERT INTO orang (nama,jk) VALUES (?,?)",
            (request.form["nama"], request.form["jk"])
        )
        con.commit()
        return redirect(request.path)
    return render_template("tambah_orang.html")

@app.route("/tambah/nikah", methods=["GET", "POST"])
def tambah_nikah():
    con = db()

    # Pisahkan laki-laki dan perempuan
    laki = con.execute("SELECT * FROM orang WHERE jk='L' ORDER BY nama").fetchall()
    perempuan = con.execute("SELECT * FROM orang WHERE jk='P' ORDER BY nama").fetchall()

    if request.method == "POST":
        suami = request.form["suami"]
        istri = request.form["istri"]
        if suami == istri:
            return "Suami dan istri tidak boleh sama!"
        con.execute(
            "INSERT INTO nikah (suami,istri) VALUES (?,?)",
            (suami, istri)
        )
        con.commit()
        return redirect(request.path)

    return render_template(
        "tambah_nikah.html",
        laki=laki,
        perempuan=perempuan
    )

@app.route("/tambah/anak", methods=["GET", "POST"])
def tambah_anak():
    con = db()

    nikah = con.execute("""
        SELECT n.id,
               o1.nama AS ayah,
               o2.nama AS ibu
        FROM nikah n
        JOIN orang o1 ON o1.id=n.suami
        JOIN orang o2 ON o2.id=n.istri
    """).fetchall()

    orang = con.execute("SELECT * FROM orang").fetchall()

    if request.method == "POST":
        nikah_id = request.form["nikah"]
        anak_id = request.form["anak"]

        pasangan = con.execute(
            "SELECT suami,istri FROM nikah WHERE id=?",
            (nikah_id,)
        ).fetchone()

        con.execute(
            "INSERT INTO ortu (anak_id,ayah,ibu) VALUES (?,?,?)",
            (anak_id, pasangan["suami"], pasangan["istri"])
        )

        con.commit()
        return redirect(request.path)

    return render_template(
        "tambah_anak.html",
        nikah=nikah,
        orang=orang
    )

# ===================== RUN =====================

if __name__ == "__main__":
    app.run(debug=True)
