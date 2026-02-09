# main.py
from flask import Flask, render_template, request, redirect, url_for
from constants import data_mahasiswa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Daftar Mahasiswa
@app.route('/daftar')
def daftar_mahasiswa():
    return render_template('daftar_mahasiswa.html', mahasiswa=data_mahasiswa.DATA)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        nilai = request.form['nilai']
        
        data_mahasiswa.DATA.append({'nim': nim, 'nama': nama, 'nilai': nilai})
        
        return redirect(url_for('daftar_mahasiswa'))
    
    return render_template('tambah_data.html')

@app.route ("/hapus/<nim>")
def hapus_data(nim):

    for mhs in data_mahasiswa.DATA:
        if mhs['nim'] == nim:
            data_mahasiswa.DATA.remove(mhs)
            break

        return redirect(url_for('daftar_mahasiswa'))
            
if __name__ == '__main__':
    app.run(debug=True)