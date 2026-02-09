from flask import Flask, render_template, request
from core.services import proses_nilai
from core.constants import dataMahasiswa

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    error = None

    # NIM selalu tersedia, bahkan sebelum submit
    nim = dataMahasiswa[0]["nim"]

    if request.method == "POST":
        try:
            daftar_nilai = [
                int(request.form["n1"]),
                int(request.form["n2"]),
                int(request.form["n3"]),
                int(request.form["n4"]),
                int(request.form["n5"]),
            ]

            hasil = proses_nilai(daftar_nilai)
        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        nim=nim,
        hasil=hasil,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
