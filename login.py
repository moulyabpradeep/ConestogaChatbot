from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import sqlite3
import smtplib
import random
import string


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Function to authenticate user login
def authenticate_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()

    conn.close()
    return user

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = authenticate_user(email, password)
    if user:
        # User authenticated, redirect to the tfa page
        return redirect(url_for('tfa', email=email))
    else:
        # User does not exist, show flash message and redirect to registration
        flash('User does not exist. Please register.')
        return redirect(url_for('register'))

def generate_verification_code():
    code_length = 4  # You can set the desired length of the code
    return ''.join(random.choices(string.digits, k=code_length))

# Function to send verification code to user's email
def send_verification_email(email, verification_code):
    sender_email = 'joel.mendonsa30@gmail.com'  # Your email address
    sender_password = 'pkhymedcjtuwnied'  # Your email password

    subject = 'Two-Factor Authentication Code'
    body = f'Your verification code is: {verification_code}'

    message = f'Subject: {subject}\n\n{body}'

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/tfa', methods=['GET', 'POST'])
def tfa():
    if request.method == 'POST':
        entered_code = request.form['verification_code']
        email = request.form.get('email')
        verification_code_sent = request.form.get('verification_code_sent')

        if entered_code == verification_code_sent:
            return redirect(url_for('success'))
        else:
            flash('Invalid verification code. Please try again.')
            return render_template('tfa.html', email=email, verification_code_sent=verification_code_sent)

    email = request.args.get('email')
    verification_code = generate_verification_code()
    email_sent = send_verification_email(email, verification_code)
    if email_sent:
        return render_template('tfa.html', email=email, verification_code_sent=verification_code)
    else:
        flash('Failed to send verification email.')
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return 'Welcome! Login successful.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email or password is empty
        if not email or not password:
            flash('Email and password are required.')
        else:
            # Add any additional validation logic here

            # Insert user into the database
            register_user(email, password)
            flash('Registration successful! You can now login.')
            return redirect(url_for('index'))  # Redirect to login page after successful registration

    return render_template('registration.html')

def register_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Insert new user into the database
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))

    conn.commit()
    conn.close()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        passcode = request.form['passcode']
        if passcode == '123456':  # Change passcode as needed
            return redirect(url_for('admin_success'))
        else:
            flash('Invalid passcode. Please try again.')
    return render_template('admin.html')

@app.route('/admin/success')
def admin_success():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Select emails and IDs from the users table
    cursor.execute('SELECT id, email FROM users')
    users_data = cursor.fetchall()

    conn.close()

    # Render admin success template with user data
    return render_template('admin_success.html', users=users_data)


if __name__ == '__main__':
    app.run(debug=True)

