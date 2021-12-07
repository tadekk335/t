from flask import Blueprint, render_template, request, redirect, url_for
from __init__ import db
from models import User
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('core.home'))
    return render_template("registration.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('core.home'))
    return render_template("login.html", user=current_user)

    
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.home"))