from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'an4231'

DB_HOST = "pgserver.mau.se"
DB_NAME = "an4231"
DB_USER = "an4231"
DB_PASS = "6umx36wl"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)


@app.route('/')
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('home.html', username=username)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            password_rs = account['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['username'] = account['username']
                session['email'] = account['email']
                return redirect(url_for('home'))
            else:
                flash('Incorrect username/password')
        else:
            flash('Incorrect username/password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        _hashed_password = generate_password_hash(password)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not password or not email or not username:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                           (username, email, _hashed_password,))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html')


@app.route('/profile')
def profile():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("select pfp from users where username = %s", (username,))
    pfp = cursor.fetchone()[0]
    return render_template('profile.html', username=username, pfp=pfp)


@app.route('/pfp', methods=['GET', 'POST'])
def pfp():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        pfp = request.form['pfp']
        cursor.execute(
            "UPDATE users SET pfp = %s WHERE username = %s;", (pfp, username,))
        conn.commit()
        cursor.close()
        return redirect(url_for('profile'))
    else:
        return render_template('pfp.html')


@app.route('/your_club')
def your_club():
    username = session['username']
    return render_template('your_club.html', username=username)


@app.route('/public_clubs')
def public_clubs():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("select title, pic, descr from book_clubs")
    book_clubs = cursor.fetchall()
    return render_template('public_clubs.html', book_clubs=book_clubs)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
