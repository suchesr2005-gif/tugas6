from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    nama = nim = None
    nilai = []
    maks = mini = None

    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']

        # ambil nilai, pisahkan dengan koma
        nilai_str = request.form['nilai']
        nilai = list(map(int, nilai_str.split(',')))

        maks = nilai[0]
        mini = nilai[0]

        for n in nilai:
            if n > maks:
                maks = n
            if n < mini:
                mini = n

    return render_template(
        'index.html',
        nama=nama,
        nim=nim,
        nilai=nilai,
        maks=maks,
        mini=mini
    )


if __name__ == "__main__":
    app.run(debug=True)
