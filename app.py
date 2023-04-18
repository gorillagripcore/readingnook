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
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            password_rs = account['password']
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

        user_desc = "Add Description!"
        pfp = "https://cdn.discordapp.com/attachments/1078973373608112128/1089867595383050291/2opekg.png"
        quote = "Forgive me, for all the things I did but mostly for the ones that I did not."
        isbn = "9781400031702"
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not password or not email or not username:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO users (username, email, password, user_desc, pfp) VALUES (%s,%s,%s,%s,%s)",(username, email, _hashed_password, user_desc, pfp))
            cursor.execute("INSERT INTO favorite_book (username, isbn) VALUES (%s, 1)",(username,))
            cursor.execute("INSERT INTO least_favorite_book (username, isbn) VALUES (%s, 2)",(username,))
            cursor.execute("INSERT INTO favorite_quote (isbn, username, quote) VALUES (%s,%s,%s)",(isbn, username, quote,))
            conn.commit()
            flash('You have successfully registered!')
            return render_template('login.html')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html')


@app.route('/profile')
def profile():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "select cover from favorite_book join books on favorite_book.isbn=books.isbn where username = %s", (username,))
    favorite_book_row = cursor.fetchone()
    if favorite_book_row is not None:
        favorite_book = favorite_book_row[0]
    else:
        favorite_book = None

    cursor.execute(
    "select favorite_book.isbn from favorite_book join books on favorite_book.isbn=books.isbn where username = %s", (username,))
    favorite_book_isbn = cursor.fetchone()[0]

    cursor.execute(
        "select cover from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (username,))
    least_favorite_book_row = cursor.fetchone()
    if least_favorite_book_row is not None:
        least_favorite_book = least_favorite_book_row[0]
    else:
        least_favorite_book = None

    cursor.execute(
    "select least_favorite_book.isbn from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (username,))
    least_favorite_book_isbn = cursor.fetchone()[0]

    cursor.execute(
        "select user_desc from users where username = %s", (username,))
    user_desc = cursor.fetchone()[0]

    cursor.execute("select pfp from users where username = %s", (username,))
    pfp = cursor.fetchone()[0]

    cursor.execute(
        "select quote from favorite_quote where username = %s", (username,))
    favorite_quote = cursor.fetchone()[0]
    cursor.execute(
        "SELECT title from books join favorite_quote on favorite_quote.isbn=books.isbn where username = %s", (username,))
    quote_book = cursor.fetchone()[0]

    return render_template('profile.html', username=username, pfp=pfp, user_desc=user_desc, favorite_book=favorite_book, favorite_book_isbn=favorite_book_isbn, least_favorite_book=least_favorite_book, least_favorite_book_isbn=least_favorite_book_isbn, favorite_quote=favorite_quote, quote_book=quote_book)


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


@app.route('/user_desc', methods=['GET', 'POST'])
def user_desc():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        user_desc = request.form['user_desc']
        cursor.execute(
            "UPDATE users SET user_desc = %s WHERE username = %s;", (user_desc, username,))
        conn.commit()
        cursor.close()
    return redirect(url_for('profile'))


@app.route('/update_fav_book', methods=['GET', 'POST'])
def update_fav_book():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        update_fav_book = request.form['update_fav_book']
        cursor.execute(
            "SELECT isbn FROM books WHERE title = %s;", (update_fav_book,))
        result = cursor.fetchone()
        if result is not None:
            isbn = result['isbn']
            cursor.execute(
                "UPDATE public.favorite_book SET isbn = %s WHERE username = %s", (isbn, username,))
            conn.commit()
            cursor.close()
            return redirect(url_for('profile'))
        else:
            flash('Book Not Found :c Make sure you capitalized the title corretly.')
    return redirect(url_for('profile'))

@app.route('/update_least_fav_book', methods=['GET', 'POST'])
def update_least_fav_book():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        update_least_fav_book = request.form['update_least_fav_book']
        cursor.execute(
            "SELECT isbn FROM books WHERE title = %s;", (update_least_fav_book,))
        result = cursor.fetchone()
        if result is not None:
            isbn = result['isbn']
            cursor.execute(
                "UPDATE public.least_favorite_book SET isbn = %s WHERE username = %s", (isbn, username,))
            conn.commit()
            cursor.close()
            return redirect(url_for('profile'))
        else:
            flash('Could not find the book. Please try again.')
    return redirect(url_for('profile'))

@app.route('/favorite_quote', methods=['GET', 'POST'])
def favorite_quote():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        quote = request.form['quote']
        book_quote = request.form['book_quote']
        cursor.execute(
            "SELECT isbn FROM books WHERE title = %s;", (book_quote,))
        result = cursor.fetchone()
        if result is not None:
            isbn = result['isbn']
            cursor.execute(
                "UPDATE favorite_quote SET isbn = %s, quote = %s WHERE username = %s", (isbn, quote, username,))
            conn.commit()
            cursor.close()
            return redirect(url_for('profile'))
        else:
            flash('Could not find the book. Please try again.')
    return redirect(url_for('profile'))

@app.route('/books/<int:book_isbn>')
def book(book_isbn):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "select * from books where isbn = %s", (book_isbn,))
    book = cursor.fetchone()

    cursor.execute(
        "select * from authors join authors_books on authors.author_id=authors_books.author_id where authors_books.isbn=%s", (book_isbn,))
    author_name = cursor.fetchone()

    conn.commit()
    cursor.close()

    return render_template('books.html', book_isbn=book_isbn, book=book, author_name=author_name)


if __name__ == "__main__":
    app.run(debug=True)
