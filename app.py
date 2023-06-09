from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


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
    value = ''
    goal_type = ''
    book_covers = []
    user_profile_pics = []
    review_book_isbns = []
    users_name = []
    reviews = None
    
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

        cursor.execute(
            'SELECT goal_type FROM public.goals where book_club = %s', (club_name))
        goal_type_row = cursor.fetchone()
        if goal_type_row is not None:
            goal_type = goal_type_row[0]
        else:
            goal_type = None

        cursor.execute(
            'SELECT value FROM public.goals where book_club = %s', (club_name))
        value_row = cursor.fetchone()
        if value_row is not None:
            value = value_row[0]
        else:
            value = None
        
        cursor.execute("SELECT * FROM reviews JOIN users ON reviews.username=users.username JOIN in_club ON in_club.username = users.username WHERE in_club.book_club=%s ORDER BY date DESC", (club_name))
        reviews = cursor.fetchall()
        if reviews is not None:
            cursor.execute("SELECT books.cover, users.pfp, reviews.book_isbn, users.username FROM books JOIN reviews ON books.isbn=reviews.book_isbn JOIN users ON reviews.username=users.username JOIN in_club ON in_club.username = users.username WHERE in_club.book_club=%s ORDER BY reviews.date DESC", (club_name))
            book_cover_rows = cursor.fetchall()

            for row in book_cover_rows:
                book_cover = row[0]
                user_profile_pic = row[1]
                review_book_isbn = row[2]
                user_name = row[3]
                book_covers.append(book_cover)
                user_profile_pics.append(user_profile_pic)
                review_book_isbns.append(review_book_isbn)
                users_name.append(user_name)
    
    else:
        user_in_club = None

    # render the template and pass the necessary data
    return render_template('home.html', username=username, user_in_club=user_in_club, book_of_the_month=book_of_the_month, book_of_the_month_title=book_of_the_month_title, book_isbn=book_isbn, date=date, time=time, location=location, value=value, goal_type=goal_type, reviews=reviews, book_covers=book_covers, user_profile_pics=user_profile_pics, review_book_isbns=review_book_isbns, users_name=users_name)

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

    cursor.execute("SELECT * FROM reviews WHERE username = %s ORDER BY date DESC", (username,))
    reviews = cursor.fetchall()

    cursor.execute("SELECT cover FROM books JOIN reviews ON books.isbn = reviews.book_isbn WHERE reviews.username = %s ORDER BY reviews.date DESC", (username,))
    book_covers = cursor.fetchall()

    # construct a list of book covers from the fetched result
    book_cover_list = [cover[0] for cover in book_covers]

    cursor.execute("SELECT book_isbn FROM reviews WHERE username = %s ORDER BY date DESC", (username,))
    review_book_isbn = cursor.fetchall()

    book_isbn_list = [book_isbn[0] for book_isbn in review_book_isbn]

    cursor.execute("SELECT isbn FROM want_to_read WHERE username = %s LIMIT 3;", (username,))
    want_to_read_isbn = cursor.fetchall() 

    isbn_list = [row[0] for row in want_to_read_isbn]

    books = {}

    for i, isbn in enumerate(isbn_list):
        cursor.execute("SELECT cover FROM books WHERE isbn = %s;", (isbn,))
        book = cursor.fetchone()

        books[f"book{i+1}"] = book

    book1 = books.get("book1")
    book2 = books.get("book2")
    book3 = books.get("book3")

    cursor.execute("SELECT book_isbn FROM reviews WHERE username = %s LIMIT 3;", (username,))
    read_isbn = cursor.fetchall() 

    read_isbn_list = [row[0] for row in read_isbn]

    read_books = {}

    for i, isbn in enumerate(read_isbn_list):
        cursor.execute("SELECT cover FROM books WHERE isbn = %s;", (isbn,))
        read_book = cursor.fetchone()

        read_books[f"read_book{i+1}"] = read_book

    book4 = read_books.get("read_book1")
    book5 = read_books.get("read_book2")
    book6 = read_books.get("read_book3")
    

    return render_template('profile.html', username=username, pfp=pfp, user_desc=user_desc, favorite_book=favorite_book, favorite_book_isbn=favorite_book_isbn, least_favorite_book=least_favorite_book, least_favorite_book_isbn=least_favorite_book_isbn, favorite_quote=favorite_quote, quote_book=quote_book, reviews=reviews, book_cover_list=book_cover_list, book_isbn_list=book_isbn_list, book1=book1, book2=book2, book3=book3, book4=book4, book5=book5, book6=book6)

@app.route('/wanttoread')
def want_to_read_page():
    username = session['username']

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT isbn FROM want_to_read WHERE username = %s;", (username,))
    read_books = cursor.fetchall()

    books = []

    #Iterate over all books in 'read_books'
    for book in read_books:
        isbn = book['isbn']
        #Get information of the book from the 'books' table using isbn
        cursor.execute("SELECT * FROM books WHERE isbn = %s;", (isbn,))
        book_info = cursor.fetchone()
        #add the book information to the 'books' list
        books.append(book_info)
    
    return render_template('want_to_read.html', username=username, books=books)

@app.route('/read')
def read_page():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT book_isbn FROM reviews WHERE username = %s;", (username,))
    read_books = cursor.fetchall()

    books = []

    #Iterate over all books in 'read_books'
    for book in read_books:
        isbn = book['book_isbn']
        #Get information of the book from the 'books' table using isbn
        cursor.execute("SELECT * FROM books WHERE isbn = %s;", (isbn,))
        book_info = cursor.fetchone()
        #add the book information to the 'books' list
        books.append(book_info)

    return render_template('read.html', username=username, books=books)


@app.route('/your_club')
def your_club():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute(
        "SELECT owner FROM book_clubs WHERE owner = %s", (username,))
    owner = cursor.fetchone()

    print(owner)

    if owner is not None and owner['owner'] == username:
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

            cursor.execute(
                'select book_of_the_month from book_club_info where title = %s', (club_name))
            book_of_the_month_isbn_row = cursor.fetchone()
            if book_of_the_month_isbn_row is not None:
                book_of_the_month_isbn = book_of_the_month_isbn_row[0]
            else:
                book_of_the_month_isbn = None

            cursor.execute(
                'SELECT goal_type FROM public.goals where book_club = %s', (club_name))
            goal_type_row = cursor.fetchone()
            if goal_type_row is not None:
                goal_type = goal_type_row[0]
            else:
                goal_type = None

            cursor.execute(
                'SELECT value FROM public.goals where book_club = %s', (club_name))
            value_row = cursor.fetchone()
            if value_row is not None:
                value = value_row[0]
            else:
                value = None

            # Fetch ongoing polls
            cursor.execute('SELECT book_club, book_1, book_2, poll_id FROM public."Poll" WHERE book_club = %s AND ongoing = True', (club_name[0],))
            ongoing_polls = cursor.fetchall()

            ongoing_covers = []

            for poll in ongoing_polls:
                book_1 = poll[1]
                book_2 = poll[2]

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_1,))
                cover_book_1 = cursor.fetchone()
                cover_book_1_url = cover_book_1[0] if cover_book_1 else None  

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_2,))
                cover_book_2 = cursor.fetchone()
                cover_book_2_url = cover_book_2[0] if cover_book_2 else None  

                ongoing_covers.append({'cover1': cover_book_1_url, 'cover2': cover_book_2_url})

            # Fetch non-ongoing polls
            cursor.execute('SELECT book_club, book_1, book_2, poll_id FROM public."Poll" WHERE book_club = %s AND ongoing = False', (club_name[0],))
            non_ongoing_polls = cursor.fetchall()

            non_ongoing_covers = []

            for poll in non_ongoing_polls:
                book_1 = poll[1]
                book_2 = poll[2]

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_1,))
                cover_book_1 = cursor.fetchone()
                cover_book_1_url = cover_book_1[0] if cover_book_1 else None  

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_2,))
                cover_book_2 = cursor.fetchone()
                cover_book_2_url = cover_book_2[0] if cover_book_2 else None  

                non_ongoing_covers.append({'cover1': cover_book_1_url, 'cover2': cover_book_2_url})

            return render_template('your_club_admin.html',username=username, club_info=club_info, members=members, book_of_the_month=book_of_the_month, location=location, date=date, time=time, book_of_the_month_isbn=book_of_the_month_isbn, goal_type=goal_type, value=value, ongoing_polls=ongoing_polls, ongoing_covers=ongoing_covers, non_ongoing_polls=non_ongoing_polls, non_ongoing_covers=non_ongoing_covers)
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

            cursor.execute(
                'select book_of_the_month from book_club_info where title = %s', (club_name))
            book_of_the_month_isbn_row = cursor.fetchone()
            if book_of_the_month_isbn_row is not None:
                book_of_the_month_isbn = book_of_the_month_isbn_row[0]
            else:
                book_of_the_month_isbn = None

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

            cursor.execute(
                'SELECT goal_type FROM public.goals where book_club = %s', (club_name))
            goal_type_row = cursor.fetchone()
            if goal_type_row is not None:
                goal_type = goal_type_row[0]
            else:
                goal_type = None

            cursor.execute(
                'SELECT value FROM public.goals where book_club = %s', (club_name))
            value_row = cursor.fetchone()
            if value_row is not None:
                value = value_row[0]
            else:
                value = None

            # Fetch ongoing polls
            cursor.execute('SELECT book_club, book_1, book_2, poll_id FROM public."Poll" WHERE book_club = %s AND ongoing = True', (club_name[0],))
            ongoing_polls = cursor.fetchall()

            ongoing_covers = []

            for poll in ongoing_polls:
                book_1 = poll[1]
                book_2 = poll[2]

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_1,))
                cover_book_1 = cursor.fetchone()
                cover_book_1_url = cover_book_1[0] if cover_book_1 else None  

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_2,))
                cover_book_2 = cursor.fetchone()
                cover_book_2_url = cover_book_2[0] if cover_book_2 else None  

                ongoing_covers.append({'cover1': cover_book_1_url, 'cover2': cover_book_2_url})

            # Fetch non-ongoing polls
            cursor.execute('SELECT book_club, book_1, book_2, poll_id FROM public."Poll" WHERE book_club = %s AND ongoing = False', (club_name[0],))
            non_ongoing_polls = cursor.fetchall()

            non_ongoing_covers = []

            for poll in non_ongoing_polls:
                book_1 = poll[1]
                book_2 = poll[2]

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_1,))
                cover_book_1 = cursor.fetchone()
                cover_book_1_url = cover_book_1[0] if cover_book_1 else None  

                cursor.execute('SELECT cover FROM books WHERE isbn = %s', (book_2,))
                cover_book_2 = cursor.fetchone()
                cover_book_2_url = cover_book_2[0] if cover_book_2 else None  

                non_ongoing_covers.append({'cover1': cover_book_1_url, 'cover2': cover_book_2_url})

            conn.commit()
            cursor.close()

            return render_template('your_club.html', username=username, club_info=club_info, members=members, book_of_the_month=book_of_the_month, location=location, date=date, time=time, book_of_the_month_isbn=book_of_the_month_isbn, goal_type=goal_type, value=value, ongoing_polls=ongoing_polls, ongoing_covers=ongoing_covers, non_ongoing_polls=non_ongoing_polls, non_ongoing_covers=non_ongoing_covers)


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

@app.route('/bcp', methods=['GET', 'POST'])
def bcp():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None 
        bcp = request.form['bcp']

        cursor.execute("UPDATE book_clubs SET pic = %s WHERE title = %s;", (bcp, book_club))
        conn.commit()
        cursor.close()
    return redirect(url_for('your_club'))

@app.route('/club_desc', methods=['GET', 'POST'])
def club_desc():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None 
        club_desc = request.form['club_desc']

        cursor.execute("UPDATE book_clubs SET descr = %s WHERE title = %s;", (club_desc, book_club))
        conn.commit()
        cursor.close()
    return redirect(url_for('your_club'))

@app.route('/botm', methods=['GET', 'POST'])
def botm():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None 
        botm = request.form['botm']

        cursor.execute(
            "SELECT isbn FROM books WHERE title = %s;", (botm,))
        result = cursor.fetchone()
        if result is not None:
            cursor.execute("UPDATE book_club_info SET book_of_the_month = %s WHERE title = %s;", (result[0], book_club,))


            conn.commit()
            cursor.close()
            return redirect(url_for('your_club'))
    return redirect(url_for('your_club'))

@app.route('/date', methods=['GET', 'POST'])
def date():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None  
        date = request.form['date']
        time = request.form['time']

        cursor.execute("UPDATE book_club_info SET meeting_date = %s WHERE title = %s;", (date, book_club,))
        cursor.execute("UPDATE book_club_info SET time = %s WHERE title = %s;", (time, book_club,))
        conn.commit()
        cursor.close()
    return redirect(url_for('your_club'))
  
@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None   
        location = request.form['location']

        cursor.execute("UPDATE book_club_info SET location = %s WHERE title = %s;", (location, book_club,))
        conn.commit()
        cursor.close()
    return redirect(url_for('your_club'))

@app.route('/member_list')
def member_list():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT book_club FROM in_club WHERE username = %s', (username,))
    book_club_row = cursor.fetchone()
    if book_club_row is not None:
        book_club = book_club_row[0]
    else:
        book_club = None 

    cursor.execute("SELECT username FROM in_club WHERE book_club = %s;", (book_club,))
    users = [user['username'] for user in cursor.fetchall()]  

    users_info = []
    for user in users:
        cursor.execute("SELECT pfp, user_desc FROM users WHERE username = %s;", (user,))
        user_info = cursor.fetchone()
        users_info.append(user_info)

    return render_template('members.html', users_info=users_info, users=users)

@app.route('/goal', methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        username = session['username']
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
        book_club_row = cursor.fetchone()
        if book_club_row is not None:
            book_club = book_club_row[0]
        else:
            book_club = None 
        goal_type = request.form['goal_type']
        number = request.form['number']

        cursor.execute('UPDATE public.goals SET goal_type = %s, value = %s WHERE book_club = %s;', (goal_type, number, book_club))
        conn.commit()
        cursor.close()
       
    return redirect(url_for('your_club'))

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
                   (username,)) 
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
    cursor.execute('DELETE FROM "Poll" WHERE book_club = %s', (club_name))
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
        goal_type = 'Books'
        value = '1'
        cursor.execute("INSERT INTO public.book_club_info(title, book_of_the_month, meeting_date, location, time) VALUES (%s, %s, %s, %s, %s)", (title, book_of_the_month, date, location, time))
        cursor.execute("INSERT INTO public.goals(book_club, goal_type, value) VALUES (%s, %s, %s)", (title, goal_type, value))
        
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
    return redirect(url_for('profile'))


@app.route('/books/<int:book_isbn>')
def book(book_isbn):
    if book_isbn in (1, 2):
        return redirect(url_for('profile'))
    username = session['username']

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "select * from books where isbn = %s", (book_isbn,))
    book = cursor.fetchone()

    cursor.execute(
        "select * from authors join authors_books on authors.author_id=authors_books.author_id where authors_books.isbn=%s", (book_isbn,))
    author_name = cursor.fetchone()

    cursor.execute("SELECT * FROM reviews WHERE username=%s and book_isbn=%s", (username, book_isbn))
    reviews = cursor.fetchone()

    cursor.execute("SELECT isbn FROM want_to_read WHERE username=%s and isbn=%s", (username, book_isbn))
    want_to_read = cursor.fetchone()

    conn.commit()
    cursor.close()

    return render_template('books.html', book_isbn=book_isbn, book=book, author_name=author_name, reviews=reviews, want_to_read=want_to_read)

@app.route('/review_book/<int:book_isbn>', methods=['POST'])
def review_book(book_isbn):
    book_isbn=book_isbn
    username = session['username']

    review_comment = request.form['review_comment']
    rating = request.form['rating']

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("INSERT INTO reviews (username, book_isbn, rating, comment, date) VALUES (%s, %s, %s, %s, %s)", (username, book_isbn, rating, review_comment, datetime.now()))

    cursor.execute("SELECT isbn FROM want_to_read WHERE username=%s and isbn=%s", (username, book_isbn))
    want_to_read = cursor.fetchone()
    
    if want_to_read != None:
        cursor.execute("DELETE FROM public.want_to_read WHERE username = %s and isbn = %s", (username, book_isbn,))

    conn.commit()

    return redirect(url_for('book', book_isbn=book_isbn))

@app.route('/want_to_read/<int:book_isbn>')
def want_to_read(book_isbn):
    book_isbn=book_isbn
    username = session['username']

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("INSERT INTO public.want_to_read(username, isbn) VALUES (%s, %s);", (username, book_isbn))
    conn.commit()

    return redirect(url_for('book', book_isbn=book_isbn))

@app.route('/edit_review/<int:book_isbn>', methods=['POST'])
def edit_review(book_isbn):
    username = session['username']

    if request.form.get('submit_edit'):
        review_comment = request.form['review_comment']
        rating = request.form['rating']

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("UPDATE reviews SET rating=%s, comment=%s, date=%s WHERE username=%s and book_isbn=%s", (rating, review_comment, datetime.now(), username, book_isbn))

        conn.commit()

    elif request.form.get('delete_review'):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("DELETE FROM reviews WHERE username=%s and book_isbn=%s", (username, book_isbn))

        conn.commit()

    return redirect(url_for('book', book_isbn=book_isbn))

@app.route('/profiles/<users>')
def profiles(users):
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "select cover from favorite_book join books on favorite_book.isbn=books.isbn where username = %s", (users,))
    favorite_book_row = cursor.fetchone()
    if favorite_book_row is not None:
        favorite_book = favorite_book_row[0]
    else:
        favorite_book = None

    cursor.execute(
        "select favorite_book.isbn from favorite_book join books on favorite_book.isbn=books.isbn where username = %s", (users,))
    favorite_book_isbn = None
    row = cursor.fetchone()
    if row is not None:
        favorite_book_isbn = row[0]

    cursor.execute(
        "select cover from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (users,))
    least_favorite_book_row = cursor.fetchone()
    if least_favorite_book_row is not None:
        least_favorite_book = least_favorite_book_row[0]
    else:
        least_favorite_book = None

    cursor.execute(
        "select least_favorite_book.isbn from least_favorite_book join books on least_favorite_book.isbn=books.isbn where username = %s", (users,))
    least_favorite_book_isbn = None
    row = cursor.fetchone()
    if row is not None:
        least_favorite_book_isbn = row[0]

    cursor.execute(
        "select user_desc from users where username = %s", (users,))
    user_desc_row = cursor.fetchone()
    if user_desc_row is not None:
        user_desc = user_desc_row[0]
    else:
        user_desc = None

    cursor.execute("select pfp from users where username = %s", (users,))
    pfp_row = cursor.fetchone()
    if pfp_row is not None:
        pfp = pfp_row[0]
    else:
        pfp = None

    cursor.execute(
        "select quote from favorite_quote where username = %s", (users,))
    favorite_quote_row = cursor.fetchone()
    if favorite_quote_row is not None:
        favorite_quote = favorite_quote_row[0]
    else:
        favorite_quote = None

    cursor.execute(
        "SELECT title from books join favorite_quote on favorite_quote.isbn=books.isbn where username = %s", (users,))
    quote_book_row = cursor.fetchone()
    if quote_book_row is not None:
        quote_book = quote_book_row[0]
    else:
        quote_book = None
    
    cursor.execute("SELECT * FROM reviews WHERE username = %s ORDER BY date DESC", (users,))
    reviews = cursor.fetchall()

    cursor.execute("SELECT cover FROM books JOIN reviews ON books.isbn = reviews.book_isbn WHERE reviews.username = %s ORDER BY reviews.date DESC", (users,))
    book_covers = cursor.fetchall()

    # Construct a list of book covers from the fetched result
    book_cover_list = [cover[0] for cover in book_covers]

    cursor.execute("SELECT book_isbn FROM reviews WHERE username = %s ORDER BY date DESC", (users,))
    review_book_isbn = cursor.fetchall()

    book_isbn_list = [book_isbn[0] for book_isbn in review_book_isbn]

    cursor.execute("SELECT isbn FROM want_to_read WHERE username = %s LIMIT 3;", (users,))
    want_to_read_isbn = cursor.fetchall() 

    isbn_list = [row[0] for row in want_to_read_isbn]

    books = {}

    for i, isbn in enumerate(isbn_list):
        cursor.execute("SELECT cover FROM books WHERE isbn = %s;", (isbn,))
        book = cursor.fetchone()

        books[f"book{i+1}"] = book

    book1 = books.get("book1")
    book2 = books.get("book2")
    book3 = books.get("book3")

    cursor.execute("SELECT book_isbn FROM reviews WHERE username = %s LIMIT 3;", (users,))
    read_isbn = cursor.fetchall() 

    read_isbn_list = [row[0] for row in read_isbn]

    read_books = {}

    for i, isbn in enumerate(read_isbn_list):
        cursor.execute("SELECT cover FROM books WHERE isbn = %s;", (isbn,))
        read_book = cursor.fetchone()

        read_books[f"read_book{i+1}"] = read_book

    book4 = read_books.get("read_book1")
    book5 = read_books.get("read_book2")
    book6 = read_books.get("read_book3")

    if username == users:
        return redirect(url_for('profile'))
    else:
        return render_template('profiles.html',  users=users, pfp=pfp, user_desc=user_desc, favorite_book=favorite_book, favorite_book_isbn=favorite_book_isbn, least_favorite_book=least_favorite_book, least_favorite_book_isbn=least_favorite_book_isbn, favorite_quote=favorite_quote, quote_book=quote_book, reviews=reviews, book_cover_list=book_cover_list, book_isbn_list=book_isbn_list, book1=book1, book2=book2, book3=book3, book4=book4, book5=book5, book6=book6)


@app.route('/poll_page/<int:poll_id>', methods=['GET'])
def poll_page(poll_id):
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT poll_id, username FROM public.voted where username = %s and poll_id = %s", (username, poll_id))
    voted = cursor.fetchone()

    #Checks if vote is not ongoing
    cursor.execute("SELECT ongoing FROM public.\"Poll\" WHERE poll_id = %s and ongoing= True", (poll_id,))
    ongoing = cursor.fetchone()

    cursor.execute("SELECT book_1 FROM public.\"Poll\" WHERE poll_id = %s", (poll_id,))
    book_1 = cursor.fetchone()

    cursor.execute("SELECT book_2 FROM public.\"Poll\" WHERE poll_id = %s", (poll_id,))
    book_2 = cursor.fetchone()

    cursor.execute("select cover from books where isbn = %s", (book_1))
    book_1_cover = cursor.fetchone()

    cursor.execute("select cover from books where isbn = %s", (book_2))
    book_2_cover = cursor.fetchone()

    cursor.execute("SELECT result_1 FROM public.\"Poll\" WHERE poll_id = %s", (poll_id,))
    result_1 = cursor.fetchone()

    cursor.execute("SELECT result_2 FROM public.\"Poll\" WHERE poll_id = %s", (poll_id,))
    result_2 = cursor.fetchone()

    cursor.execute("SELECT owner FROM book_clubs WHERE owner = %s", (username,))
    owner = cursor.fetchone()
        
    return render_template('poll.html', voted=voted, book_1_cover=book_1_cover, book_2_cover=book_2_cover, poll_id=poll_id, result_1=result_1, result_2=result_2, ongoing=ongoing, username=username, owner=owner)

@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    selected_option = request.form.get('vote')

    # Add that the user voted on it so that they can't vote again
    cursor.execute("INSERT INTO public.voted(poll_id, username) VALUES (%s, %s);", (poll_id, username))

    if selected_option == 'book_1':
        cursor.execute("SELECT result_1 FROM public.\"Poll\" WHERE poll_id = %s;", (poll_id,))
        result = cursor.fetchone()

        if result is not None:
            result = result['result_1'] + 1
        else:
            result = 1

        cursor.execute("UPDATE public.\"Poll\" SET result_1 = %s WHERE poll_id = %s;", (result, poll_id))

    elif selected_option == 'book_2':
        cursor.execute("SELECT result_2 FROM public.\"Poll\" WHERE poll_id = %s;", (poll_id,))
        result = cursor.fetchone()

        if result is not None:
            result = result['result_2'] + 1
        else:
            result = 1

        cursor.execute("UPDATE public.\"Poll\" SET result_2 = %s WHERE poll_id = %s;", (result, poll_id))

    return redirect(url_for('poll_page', poll_id=poll_id))

@app.route('/endvote/<int:poll_id>', methods=['POST'])
def endvote(poll_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('UPDATE public."Poll" SET ongoing=false WHERE poll_id = %s;', (poll_id,))


    return redirect(url_for('poll_page', poll_id=poll_id))


@app.route('/create_poll')
def create_poll():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT book_club FROM in_club WHERE username = %s', (username,))
    book_club_row = cursor.fetchone()
    if book_club_row is not None:
        book_club = book_club_row[0]
    else:
        book_club = None
  
    return render_template('create_poll.html', book_club=book_club, )

@app.route('/create_poll_submit', methods=['POST'])
def create_poll_submit():
    username = session['username']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT title FROM book_clubs WHERE owner = %s', (username,))
    book_club_row = cursor.fetchone()
    if book_club_row is not None:
        book_club = book_club_row[0]
    else:
        book_club = None

    book_1 = request.form.get('book_1')
    book_2 = request.form.get('book_2')

    result_1 = 0
    result_2 = 0
    ongoing = True

    cursor.execute('SELECT isbn FROM books where title = %s', (book_1,))
    book_1_row = cursor.fetchone()
    if book_1_row is not None:
        book_1 = book_1_row['isbn']
    else:
        book_1 = None

    cursor.execute('SELECT isbn FROM books where title = %s', (book_2,))
    book_2_row = cursor.fetchone()
    if book_2_row is not None:
        book_2 = book_2_row['isbn']
    else:
        book_2 = None
    
    if book_1 and book_2 != None:
         cursor.execute('INSERT INTO public.\"Poll\" (book_club, book_1, book_2, result_1, result_2, ongoing) VALUES (%s, %s, %s, %s, %s, %s);', (book_club, book_1, book_2, result_1, result_2, ongoing))
    else: 
        pass
    return redirect(url_for('your_club'))


if __name__ == "__main__":
    app.run(debug=True)
