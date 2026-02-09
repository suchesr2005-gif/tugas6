from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home/<nama>')
def home_name(nama):
    return render_template('home.html', nama=nama)

if __name__ == '__main__':
    app.run(debug=True)