from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email ).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category= 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='eror')
        else :
            flash('User does not exist', category = 'error' )
                 
    return render_template("login.html", user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email= request.form.get('email')
        fullname= request.form.get('fullname')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        
        user = User.query.filter_by(email = email).first()
        
        if user:
            flash('User already exist', category= 'error')
        elif len(email)< 10:
            flash('Email is too short!', category='error')
        elif len(fullname)< 5:
            flash(' Name is too short', category='error')
        elif len(password)< 7:
            flash('password is too short!', category='error')
        elif password != confirmpassword:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(email=email, fullname=fullname, password=generate_password_hash(password, method='sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("signup.html", user=current_user)
