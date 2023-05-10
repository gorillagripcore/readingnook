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

    book_of_the_month = None
    book_of_the_month_title = ''
    book_isbn = None
    date = None
    time = ''
    location = ''
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('SELECT * FROM in_club WHERE username=%s', (username,))
    user_in_club = cursor.fetchone()
    if user_in_club is not None:
        cursor.execute(
            "SELECT book_club FROM in_club WHERE username=%s", (username,))
        club_name = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM books join book_club_info ON books.isbn=book_club_info.book_of_the_month WHERE book_club_info.title = %s", (club_name))
        book_of_the_month_row = cursor.fetchone()
        if book_of_the_month_row is not None:
            book_of_the_month = book_of_the_month_row[2]
            book_of_the_month_title = book_of_the_month_row[1]
        
        cursor.execute("SELECT * FROM book_club_info WHERE title = %s", (club_name))
        date_row = cursor.fetchone()
        if date_row is not None:
            date = date_row[2]
            time = date_row[4]
            location = date_row[3]

        cursor.execute(
        "SELECT books.isbn FROM books join book_club_info ON books.isbn=book_club_info.book_of_the_month WHERE book_club_info.title = %s", (club_name))
        book_isbn_row = cursor.fetchone()
        if book_isbn_row is not None:
            book_isbn = book_isbn_row[0]
    else:
        user_in_club = None
    conn.commit()
    cursor.close()
    return render_template('home.html', username=username, user_in_club=user_in_club, book_of_the_month=book_of_the_month, book_of_the_month_title=book_of_the_month_title, book_isbn=book_isbn, date=date, time=time, location=location) 


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
            cursor.execute("INSERT INTO users (username, email, password, user_desc, pfp) VALUES (%s,%s,%s,%s,%s)",
                           (username, email, _hashed_password, user_desc, pfp))
            cursor.execute(
                "INSERT INTO favorite_book (username, isbn) VALUES (%s, 1)", (username,))
            cursor.execute(
                "INSERT INTO least_favorite_book (username, isbn) VALUES (%s, 2)", (username,))
            cursor.execute(
                "INSERT INTO favorite_quote (isbn, username, quote) VALUES (%s,%s,%s)", (isbn, username, quote,))
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
    favorite_book_isbn = None
    row = cursor.fetchone()
    if row is not None:
        favorite_book_isbn = row[0]

    cursor.execute(
        "select cover from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (username,))
    least_favorite_book_row = cursor.fetchone()
    if least_favorite_book_row is not None:
        least_favorite_book = least_favorite_book_row[0]
    else:
        least_favorite_book = None

    cursor.execute(
        "select least_favorite_book.isbn from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (username,))
    least_favorite_book_isbn = None
    row = cursor.fetchone()
    if row is not None:
        least_favorite_book_isbn = row[0]

    cursor.execute(
        "select user_desc from users where username = %s", (username,))
    user_desc_row = cursor.fetchone()
    if user_desc_row is not None:
        user_desc = user_desc_row[0]
    else:
        user_desc = None

    cursor.execute("select pfp from users where username = %s", (username,))
    pfp_row = cursor.fetchone()
    if pfp_row is not None:
        pfp = pfp_row[0]
    else:
        pfp = None

    cursor.execute(
        "select quote from favorite_quote where username = %s", (username,))
    favorite_quote_row = cursor.fetchone()
    if favorite_quote_row is not None:
        favorite_quote = favorite_quote_row[0]
    else:
        favorite_quote = None

    cursor.execute(
        "SELECT title from books join favorite_quote on favorite_quote.isbn=books.isbn where username = %s", (username,))
    quote_book_row = cursor.fetchone()
    if quote_book_row is not None:
        quote_book = quote_book_row[0]
    else:
        quote_book = None

    return render_template('profile.html', username=username, pfp=pfp, user_desc=user_desc, favorite_book=favorite_book, favorite_book_isbn=favorite_book_isbn, least_favorite_book=least_favorite_book, least_favorite_book_isbn=least_favorite_book_isbn, favorite_quote=favorite_quote, quote_book=quote_book)


@app.route('/your_club')
def your_club():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute(
        "SELECT owner FROM book_clubs WHERE owner=%s", (username,))
    owner = cursor.fetchone()

    if owner is None:

        cursor.execute(
            "SELECT * FROM book_clubs JOIN in_club ON book_clubs.title=in_club.book_club WHERE username=%s", (username,))
        club_info = cursor.fetchone()

        cursor.execute(
            "SELECT book_club from in_club WHERE username=%s", (username,))
        club_name = cursor.fetchone()

        cursor.execute(
            'select count(username)from in_club where book_club = %s', (club_name))
        members_row = cursor.fetchone()
        if members_row is not None:
            members = members_row[0]
        else:
            members = None

        cursor.execute(
            'select cover from books join book_club_info on books.isbn=book_club_info.book_of_the_month where book_club_info.title = %s', (club_name))
        book_of_the_month_row = cursor.fetchone()
        if book_of_the_month_row is not None:
            book_of_the_month = book_of_the_month_row[0]
        else:
            book_of_the_month = None

        cursor.execute('select meeting_date from book_club_info where title = %s', (club_name))
        date_row = cursor.fetchone()
        if date_row is not None:
            date = date_row[0]
        else:
            date = None

        cursor.execute('select time from book_club_info where title = %s', (club_name))
        time_row = cursor.fetchone()
        if time_row is not None:
            time = time_row[0]
        else:
            time = None
        
        cursor.execute(
            'select location from book_club_info where title = %s', (club_name))
        location_row = cursor.fetchone()
        if location_row is not None:
            location = location_row[0]
        else:
            location = None

        conn.commit()
        cursor.close()

        return render_template('your_club.html', username=username, club_info=club_info, members=members, book_of_the_month=book_of_the_month, location=location, date=date, time=time,)
    else: 
        cursor.execute(
            "SELECT * FROM book_clubs JOIN in_club ON book_clubs.title=in_club.book_club WHERE username=%s", (username,))
        club_info = cursor.fetchone()

        cursor.execute(
            "SELECT book_club from in_club WHERE username=%s", (username,))
        club_name = cursor.fetchone()

        cursor.execute(
            'select count(username)from in_club where book_club = %s', (club_name))
        members_row = cursor.fetchone()
        if members_row is not None:
            members = members_row[0]
        else:
            members = None

        cursor.execute(
            'select cover from books join book_club_info on books.isbn=book_club_info.book_of_the_month where book_club_info.title = %s', (club_name))
        book_of_the_month_row = cursor.fetchone()
        if book_of_the_month_row is not None:
            book_of_the_month = book_of_the_month_row[0]
        else:
            book_of_the_month = None

        cursor.execute('select meeting_date from book_club_info where title = %s', (club_name))
        date_row = cursor.fetchone()
        if date_row is not None:
            date = date_row[0]
        else:
            date = None

        cursor.execute('select time from book_club_info where title = %s', (club_name))
        time_row = cursor.fetchone()
        if time_row is not None:
            time = time_row[0]
        else:
            time = None
        
        cursor.execute(
            'select location from book_club_info where title = %s', (club_name))
        location_row = cursor.fetchone()
        if location_row is not None:
            location = location_row[0]
        else:
            location = None

        conn.commit()
        cursor.close()

        return render_template('your_club_admin.html', username=username, club_info=club_info, members=members, book_of_the_month=book_of_the_month, location=location, date=date, time=time,)
    
@app.route('/admin_suggestions', methods=['GET', 'POST'])
def admin_suggestions():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT title FROM book_clubs where owner = %s", (username,))
    book_club_title_row = cursor.fetchone()
    if book_club_title_row is not None:
        book_club_title = book_club_title_row[0]
    else:
        book_club_title = None


    cursor.execute( "SELECT book_title, author FROM suggestion_box where book_club = %s", (book_club_title,))
    suggestions = cursor.fetchall()
    
    print(suggestions)
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/suggest_book', methods=['GET', 'POST'])
def suggest_book():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT book_club FROM in_club where username = %s", (username,))
    book_club_name_row = cursor.fetchone()
    if book_club_name_row is not None:
        book_club_name = book_club_name_row[0]
    else:
        book_club_name = None


    suggested_title = request.form['titel_suggestion']
    suggested_author = request.form['author_suggestion']
        
    cursor.execute("INSERT INTO public.suggestion_box( book_club, book_title, author) VALUES (%s, %s, %s);", (book_club_name, suggested_title, suggested_author))
        
    conn.commit()
    cursor.close()
    return redirect(url_for('your_club'))


    
@app.route('/public_clubs')
def public_clubs():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT title, pic, descr FROM book_clubs")
    book_clubs = cursor.fetchall()

    book_club_title = request.form.get('book_club_title')
    username = session['username']
    cursor.execute('SELECT * FROM in_club WHERE username=%s', (username,))
    user_in_club = cursor.fetchone()
    if user_in_club:
        return redirect(url_for('your_club'))
    else:
        cursor.execute(
            "SELECT * FROM book_clubs WHERE title = %s", (book_club_title,))
        book_club_title = None
        row = cursor.fetchone()
        if row is not None:
            book_club_title = row[0]
    return render_template('public_clubs.html', book_clubs=book_clubs)
    

@app.route('/join_club', methods=['GET', 'POST'])
def join_club():
    if request.method == 'POST':
        book_club_title = request.form.get('book_club_title')
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("INSERT INTO in_club VALUES (%s, %s)",
                       (username, book_club_title))
        conn.commit()
        return redirect(url_for('your_club'))
    else:
        return redirect(url_for('home.html'))


@app.route('/leave_club', methods=['GET', 'POST'])
def leave_club():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM in_club WHERE username = %s",
                   (username,))  # den
    conn.commit()
    return redirect(url_for('public_clubs'))

@app.route('/delete_club', methods=['GET', 'POST'])
def delete_club():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT book_club FROM in_club WHERE username=%s', (username,))
    club_name= cursor.fetchone()

    cursor.execute("DELETE FROM in_club WHERE book_club = %s", (club_name))
    cursor.execute("DELETE FROM public.book_club_info WHERE title = %s", (club_name))
    cursor.execute("DELETE FROM suggestion_box WHERE book_club = %s", (club_name))
    cursor.execute("DELETE FROM book_clubs WHERE owner = %s", (username,))
    conn.commit()
    return redirect(url_for('public_clubs'))


@app.route('/create_club', methods=['GET', 'POST'])
def create_club():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        title = request.form['name']
        club_picture = request.form['club_picture']
        club_desc = request.form['club_desc']
        
        cursor.execute("INSERT INTO public.book_clubs(title, descr, owner, pic) VALUES (%s, %s, %s, %s);", (title, club_desc, username, club_picture,))
        cursor.execute("INSERT INTO in_club VALUES (%s, %s)", (username, title))
        
        book_of_the_month = '9780140449174'
        date = "0001-01-01"
        location = 'Malmö, Sweden'
        time = '00:00'
        cursor.execute("INSERT INTO public.book_club_info(title, book_of_the_month, meeting_date, location, time) VALUES (%s, %s, %s, %s, %s)", (title, book_of_the_month, date, location, time))
        conn.commit()
        cursor.close()
        return redirect(url_for('your_club'))
    return render_template('create_club.html')


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
    if book_isbn in (1, 2):
        return redirect(url_for('profile'))

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
