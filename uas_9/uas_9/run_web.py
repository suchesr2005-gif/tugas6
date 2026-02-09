from flask import Flask, render_template, request
from core.constants import nilai
from core.services import hitung_kelulusan, hitung_ambang_batas

app = Flask(__name__)

@app.route('/')
def hitung():
    hasil, hasil2 = hitung_kelulusan()
    return render_template('nilai.html', 
                           nilai=nilai,  
                           hasil=hasil,
                           hasil2=hasil2)

@app.route('/no_2', methods=["GET", "POST"])
def hitung2():
    hasil=hasil2=None

    if request.method == "POST":
        th1 = request.form["threshold1"]
        th2 = request.form["threshold2"]

        th1 = int(th1)
        th2 = int(th2)

        hasil, hasil2 = hitung_ambang_batas(threshold1=th1, threshold2=th2)

    return render_template('no_2.html',
                           hasil=hasil,
                           hasil2=hasil2,
                           nilai=nilai
                           )


if __name__ == '__main__':
    app.run(debug=True)

