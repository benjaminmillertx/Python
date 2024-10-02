FlaskSimple Framework

Project Name: FlaskSimple
Key Features

    Password Hashing: Securely hash passwords using werkzeug.security.
    Advanced Validation: Improve input validation using Flask-WTF.
    Session Management: Utilize Flask-Login for user session handling.
    RESTful API: Add endpoints for user registration and message handling.
    Error Handling: Implement error handling to manage exceptions gracefully.
    Complex Data Interactions: Provide more advanced querying and data handling mechanisms.

Complete Code 



from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class MinimalWebFramework:
    def __init__(self, name):
        self.app = Flask(name)
        self.app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
        self.db_name = 'app.db'
        self.initialize_db()
        
        # Initialize Flask-Login
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'login'

    def initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

    def route(self, path, methods=['GET']):
        def wrapper(func):
            self.app.add_url_rule(path, func.__name__, func, methods=methods)
            return func
        return wrapper

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def render(self, template_string, **context):
        return render_template_string(template_string, **context)

# Create an instance of the web framework
app = MinimalWebFramework(__name__)

# Configure user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load user function for Flask-Login
@app.login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect(app.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return User(result[0]) if result else None

# Flask-WTF forms with advanced validation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Send')

# CSS styles
CSS = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        color: #333;
        margin: 0;
        padding: 20px;
    }
    h1 {
        color: #007bff;
        text-align: center;
    }
    .container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .btn, .form-control {
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
        border: 1px solid #007bff;
        margin-top: 10px;
        display: block;
        width: calc(100% - 22px);
    }
    .btn {
        background-color: #007bff;
        color: white;
        text-decoration: none;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #0056b3;
    }
    textarea {
        resize: vertical;
    }
</style>
"""

# Example templates
index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlaskSimple</title>
    {css}
</head>
<body>
    <div class="container">
        <h1>Welcome to FlaskSimple!</h1>
        {% if not current_user.is_authenticated %}
            <a href="/login" class="btn">Login</a>
            <a href="/register" class="btn">Register</a>
        {% else %}
            <h2>Hello, {{ current_user.id }}!</h2>
            <form method="POST" action="/send">
                <textarea name="message" class="form-control" rows="4" placeholder="Your Message" required></textarea>
                <button type="submit" class="btn">Send</button>
            </form>
            <a href="/logout" class="btn">Logout</a>
        {% endif %}
        <h2>Messages</h2>
        <ul>
            {% for msg in messages %}
                <li><strong>User {{ msg[1] }}:</strong> {{ msg[2] }} ({{ msg[3] }})</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

register_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - FlaskSimple</title>
    {css}
</head>
<body>
    <div class="container">
        <h1>Register</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username(size=32) }}<br>
            {{ form.password.label }} {{ form.password(size=32) }}<br>
            {{ form.confirm_password.label }} {{ form.confirm_password(size=32) }}<br>
            {{ form.submit() }}
        </form>
        <a href="/" class="btn">Back Home</a>
    </div>
</body>
</html>
"""

login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - FlaskSimple</title>
    {css}
</head>
<body>
    <div class="container">
        <h1>Login</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username(size=32) }}<br>
            {{ form.password.label }} {{ form.password(size=32) }}<br>
            {{ form.submit() }}
        </form>
        <a href="/" class="btn">Back Home</a>
    </div>
</body>
</html>
"""

# Error handling middleware
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

# Define routes
@app.route('/')
def home():
    with sqlite3.connect(app.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, message, created_at FROM messages")
        messages = cursor.fetchall()
    return app.render(index_template.format(css=CSS, messages=messages))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        with sqlite3.connect(app.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                               (username, password))
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists. Please choose a different one.', 'danger')
    return app.render(register_template.format(css=CSS, form=form))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        with sqlite3.connect(app.db_name) as conn:
            cursor = conn.cursor()
            user = cursor.execute("SELECT id, password FROM users WHERE username = ?", 
                                  (username,)).fetchone()
            if user and check_password_hash(user[1], password):
                login_user(User(user[0]))
                flash('Welcome back!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.', 'danger')
    return app.render(login_template.format(css=CSS, form=form))

@app.route('/send', methods=['POST'])
@login_required
def send():
    form = MessageForm()
    if form.validate_on_submit():
        message = form.message.data
        try:
            with sqlite3.connect(app.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", 
                               (current_user.id, message))
                conn.commit()
        except Exception as e:
            flash('Error sending message: ' + str(e), 'danger')
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# RESTful API section
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    try:
        with sqlite3.connect(app.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (username, password))
            conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists.'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['POST'])
@login_required
def api_send_message():
    data = request.json
    message = data.get('message')
    if len(message) > 200:
        return jsonify({'error': 'Message exceeds 200 characters.'}), 400
    try:
        with sqlite3.connect(app.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", 
                           (current_user.id, message))
            conn.commit()
        return jsonify({'message': 'Message sent!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

Licensing
GNU General Public License

This project is licensed under the GNU General Public License (GPL). You are free to use, modify, and distribute this code with or without changes under the same license.

Full License Text:
text

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) <year> Free Software Foundation, Inc.
<https://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
...

[Continue with complete GPL text]

You can find the full text of the GNU GPL here

.
Documentation
1. Setup

    Ensure you have Python and pip installed.

    Install the required packages:
    bash

    pip install Flask Flask-Login Flask-WTF Werkzeug

2. Run the Application

    Save the code above in a file called app.py.

    Run the application:
    bash

    python app.py

3. Accessing the Application

    Open your web browser and go to http://127.0.0.1:5000/.

4. User Registration and Login

    To register a new user, navigate to http://127.0.0.1:5000/register.
    Passwords must be at least 6 characters long and will be hashed for security.
    After registration, log in at http://127.0.0.1:5000/login.

5. Sending Messages

    Once logged in, you can send messages (limited to 200 characters) that will be displayed on the home page under your session.
    If there’s an issue when sending, an error message will show.

6. Error Handling

    The application includes error handling for both the web and API endpoints.
    If the application encounters an error, it will return a JSON response with the error message and HTTP status code.

7. RESTful API Documentation

    User Registration:
        Endpoint: /api/register
        Method: POST
        Request:
        json

    {
      "username": "your_username",
      "password": "your_password"
    }

    Response:
        201 Created: User registered successfully.
        409 Conflict: Username already exists.
        500 Internal Server Error: An unexpected error occurred.

Send Message:

    Endpoint: /api/messages
    Method: POST
    Authorization: Requires user to be logged in (session token).
    Request:
    json

{
  "message": "Your message here"
}

Response:

    201 Created: Message sent successfully.
    400 Bad Request: Message exceeds character limit.
    500 Internal Server Error: An unexpected error occurred.

