#app.py


from flask import Flask, render_template, request, session, redirect
from controller.parkir_controller import proses, tampil_menu

app = Flask(__name__)
app.secret_key = "parkir-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if "step" not in session:
        session.clear()
        session["step"] = "menu"
        session["log"] = []
        tampil_menu()

    if request.method == "POST":
        input_user = request.form.get("input", "")
        hasil_proses = proses(input_user)

        if hasil_proses == "reset":
            return redirect("/")

        return redirect("/")

    labels = {
        "menu": "Pilihan : ",
        "plat": "Plat : ",
        "jenis": "Jenis : ",
        "merk": "Merk : ",
        "keluar": "Plat Kendaraan : ",
        "pause": ""
    }

    return render_template(
        "index.html",
        log=session.get("log", []),
        label=labels.get(session.get("step"), "")
    )

if __name__ == "__main__":
    app.run(debug=True)
