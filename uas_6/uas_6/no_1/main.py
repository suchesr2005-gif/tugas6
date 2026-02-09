from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = "rahasia_login"

USERS = {
    "admin": "123",
    "user": "123"
}

# 🔐 LOGIN (GERBANG UTAMA)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("Username atau password salah!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login-error')
def login_error():
    return render_template('login_error.html')


# 🏠 HOME (SETELAH LOGIN)
@app.route('/')
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


# 📄 INDEX
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['nama'] = request.form['nama']
        session['nim'] = request.form['nim']
        session['nilai'] = list(map(int, request.form['nilai'].split(',')))

    nilai = session.get('nilai', [])
    maks = mini = None
    if nilai:
        maks = max(nilai)
        mini = min(nilai)

    return render_template(
        'index.html',
        user=session['user'],
        nama=session.get('nama'),
        nim=session.get('nim'),
        nilai=nilai,
        maks=maks,
        mini=mini
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
