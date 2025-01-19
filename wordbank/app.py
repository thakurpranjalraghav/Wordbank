# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['is_admin'] = user[4]
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        word = request.form['word']
        meaning = request.form['meaning']
        language = request.form['language']
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO words (word, meaning, language, user_id) VALUES (%s, %s, %s, %s)", (word, meaning, language, user_id))
        mysql.connection.commit()
        flash('Word added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_word.html')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('index'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM words")
    words = cursor.fetchall()
    return render_template('admin.html', words=words)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
