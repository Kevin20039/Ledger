from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        if 'signup' in request.form:
            # Registration Logic
            username = request.form.get('username')
            password = request.form.get('password')
            business_name = request.form.get('business_name')
            
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.', 'error')
            else:
                new_user = User(username=username, password=generate_password_hash(password), business_name=business_name)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('main.dashboard'))
                
        else:
            # Login Logic
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash('Incorrect username or password.', 'error')
                
    return render_template('auth.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
