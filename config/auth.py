from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import Person
from config.config import SessionLocal
from flask_wtf.csrf import CSRFProtect

auth_bp = Blueprint('auth', __name__)
csrf = CSRFProtect()

def authenticate_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(Person).filter_by(username=username).first()
        if not user:
            return None, "Username does not exist"
        if not check_password_hash(user.password_hash, password):  
            return None, "Incorrect password"
        return user, None
    finally:
        db.close()

def register_user(username, email, password, role='user'):
    db = SessionLocal()
    try:
        # Перевірка наявності обов'язкових полів
        if not username or not email or not password:
            return False, "All fields are required"
        
        # Перевірка унікальності користувача
        if db.query(Person).filter_by(username=username).first():
            return False, "Username already exists"
        if db.query(Person).filter_by(email=email).first():
            return False, "Email already exists"
        
        # Реєстрація нового користувача
        new_user = Person(username=username, email=email, role=role)
        new_user.set_password(password)  # Corrected to use set_password method
        db.add(new_user)
        db.commit()
        return True, "Registration successful"
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    db = SessionLocal()
    user = db.query(Person).get(user_id)
    return render_template('profile.html', user=user)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user, error = authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['user_type'] = user.role
            return redirect(url_for('auth.profile'))  # Corrected redirect URL
        else:
            flash(error)
            return redirect(url_for('auth.login'))
    
    return render_template('profile.html', form_type='login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')
        
        success, message = register_user(username, email, password, role)  # Removed redundant hashing

        if success:
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        else:
            flash(message)
            return redirect(url_for('auth.register'))
    
    return render_template('profile.html', form_type='register')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))