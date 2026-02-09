from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    nama = None
    if request.method == 'POST':
        nama = request.form.get('nama')
    return render_template('home.html', nama=nama)

if __name__ == '__main__':
    app.run(debug=True)