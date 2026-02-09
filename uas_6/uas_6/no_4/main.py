from flask import Flask, render_template
import constants

app = Flask(__name__)

@app.route('/')
def main():
    data = constants.biodata[0]
    
    nama = data['nama']
    nim = data['nim'] 

    nilai = constants.nilai

    maks = nilai[0]
    mini = nilai[0]

    for n in nilai:
        if n > maks:
            maks = n
        if n < mini:
            mini = n

    return render_template('index.html', 
                           nama=nama, 
                           nim=nim, 
                           nilai=nilai,
                           maks=maks, mini=mini)



if __name__ == "__main__":
    app.run(debug=True)
