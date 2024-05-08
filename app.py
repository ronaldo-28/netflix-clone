import secrets
from flask import Flask, render_template, request, redirect, url_for,session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import or_
from flask_migrate import Migrate


app = Flask(__name__)
secret_key = secrets.token_hex(16)  # Generate a 16-byte (32-character) random hexadecimal string
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ownername:password@localhost/database_name'  # Replace with your PostgreSQL URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)

def init_db():
    with app.app_context():
    # Create all database tables
        db.create_all()

from flask import request

@app.route('/')
def home():
    # Get the email from the request parameters
    email = request.args.get('email', '')  # If the 'email' parameter is not present, default to an empty string
    
    # Render the homepage with the email parameter included in the URL
    return render_template('index.html', email=email)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database for the user
        user = User.query.filter_by(email=email).first()
        
        # Check if the user exists and the password is correct
        if user and user.password == password:
            # Set session variables for user_id and is_superuser
            session['user_id'] = user.id
            session['is_superuser'] = user.is_superuser
            
            # Redirect to appropriate page based on superuser status
            if user.is_superuser:
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('moviepage'))
        else:
            # Authentication failed, show sign-in page with an error message
            error_message = 'Invalid Email or Password'
            return render_template('signin.html', error=error_message)
    else:
        # If the request method is GET, simply render the sign-in page
        return render_template('signin.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, allow access to the route
            return f(*args, **kwargs)
        else:
            # User is not logged in, redirect to the sign-in page
            return redirect(url_for('signin'))
    return decorated_function

@app.route('/moviepage')
@login_required
def moviepage():
    # Render the moviepage.html page
    return render_template('moviepage.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, allow access to the route
            return f(*args, **kwargs)
        else:
            # User is not logged in, redirect to the sign-in page
            return redirect(url_for('signin'))
    return decorated_function

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the home page or any other desired page
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the email or username is already registered
        if User.query.filter_by(email=email).first() is not None:
            error_message = 'Email already registered'
            return render_template('register.html', error=error_message)
        if User.query.filter_by(username=username).first() is not None:
            error_message = 'Username already registered'
            return render_template('register.html', error=error_message)

        # Create a new user object and add it to the database
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    else:
        # If the request method is GET, simply render the registration form
        return render_template('register.html')
    
@app.route('/register_superadmin', methods=['GET', 'POST'])
def register_superadmin():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if any users exist in the database
        user_exists = User.query.first()

        # If no user exists, designate the first registered user as superuser
        is_superuser = False
        if not user_exists:
            is_superuser = True

        # Check if the email or username is already registered
        if User.query.filter(or_(User.email == email, User.username == username)).first() is not None:
            error_message = 'Email or Username already registered'
            return render_template('register_superadmin.html', error=error_message)

        # Create a new user object and add it to the database
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin'))
    else:
        return render_template('register_superadmin.html')
    
def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and is a superuser
        if 'user_id' in session and 'is_superuser' in session and session['is_superuser']:
            return f(*args, **kwargs)
        else:
            # If not a superuser, redirect to the sign-in page
            return redirect(url_for('signin'))
    return decorated_function

@app.route('/admin')
@superuser_required
def admin_panel():
    # Fetch all superusers from the database
    superusers = User.query.filter_by(is_superuser=True).all()
    return render_template('admin_panel.html', superusers=superusers)

@app.route('/admin/add_superuser', methods=['GET', 'POST'])
def add_superuser():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Create a new user object and add it to the database with is_superuser set to True
        new_user = User(email=email, username=username, password=password, is_superuser=True)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin_panel'))
    else:
        return render_template('add_superuser.html')

@app.route('/adminlogout', methods=['POST'])
def adminlogout():
    # Clear the session data
    session.clear()
    # Redirect to the home page or any other desired page
    return redirect(url_for('home'))



if __name__ == '__main__':
    # Initialize the database before running the app
    init_db()
    
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

