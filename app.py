from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
app.secret_key = 'an4231'
 
DB_HOST = "pgserver.mau.se"
DB_NAME = "an4231"
DB_USER = "an4231"
DB_PASS = "6umx36wl"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def home():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cursor.execute("select distinct(product_name), base_price, supplier_name, count(product_name) as amount from products join suppliers on suppliers.supplier_id=products.supplier_id group by base_price, product_name, supplier_name")
    #data = cursor.fetchall()
    #if 'loggedin' in session:
        #if session['is_admin'] == True:
            #return render_template('home_admin.html', email=session['email'], is_admin=session['is_admin'], data=data )
        #else:
            #return render_template('home_user.html', email=session['email'], data=data)
    return render_template('home.html')#, data=data)

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
        #elif not password or not email or not username:
            #flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)", (username, email, _hashed_password,))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)