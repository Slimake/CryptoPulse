#!/usr/bin/python3
from api.v1.views import app_views_auth
from models.user import User
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
import bcrypt
from models.user import User
from models import storage
from uuid import uuid4


@app_views_auth.route('/login', methods=['GET', 'POST'])
def login():
     cache_id = uuid4()
     if request.method == 'POST':
          username = request.form['username'] #Ask the guys if we want to use email or username to login
          password = request.form['password']
          remember = True if request.form.get('remember') else False

          # Fetch user data from database
          user = storage.get_username(User, username)

          if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
               login_user(user, remember=remember)
               return redirect(url_for('app_views_main.index'))
          else:
               flash('Invalid username or password!')

     return render_template('login.html', cache_id=cache_id)

@app_views_auth.route('/signup', methods=['GET', 'POST'])
def signup():
     cache_id = uuid4()
     if request.method == 'POST':
          email = request.form.get('email')
          username = request.form.get('username')
          password = request.form.get('password')
          confirm_password = request.form.get('confirm_password')

          user = storage.get_username(User, username)
          email_check = storage.get_email(User, email)
          
          # Validation check
          if user is not None and user.username == username:
               flash('Username already exists!')
               return redirect(url_for('app_views_auth.signup'))
          elif email_check is not None and email_check.email == email:
               flash('Email already exists')
               return redirect(url_for('app_views_auth.signup'))
          elif password != confirm_password:
               flash('Password and Confirm Password do not match!')
               return redirect(url_for('app_views_auth.signup'))
          else:
               password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
               new_user = User(email=email, username=username, password_hash=password_hash)

               #Saving new_user to DBStorage
               new_user.save()

               flash('Succefully signed up! Please log in.', 'success')
               return redirect(url_for('app_views_auth.login'))
          
     return render_template('signup.html', cache_id=cache_id)


@app_views_auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile"""
    cache_id = uuid4() # generate random uuid
    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        username = current_user.username
        user = storage.get_username(User, username)
        new_email_check = storage.get_email(User, email)
        user_email = storage.get_email(User, user.email)


        # Validation check
        if user_email.email != email and new_email_check is not None:
            flash('Email already exists, Choose another email', 'error')
            return redirect(url_for('app_views_auth.profile'))
        elif user_email.email != email and new_email_check is None:
            user.email = email
    
        if old_password and new_password:
            if old_password == new_password:
                flash('New Password cannot be same as Old Password!', 'error')
                return redirect(url_for('app_views_auth.profile'))
            elif not bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    flash('Old password is incorrect', 'error')
                    return redirect(url_for('app_views_auth.profile'))

            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = password_hash
        new_user = User(**user.to_dict())

        if user_email.email == email:
            #Saving new_user to DBStorage
            new_user.save()

            flash('Succefully saved.', 'success')
            return redirect(url_for('app_views_auth.profile'))
        elif not old_password:
            flash('Old Password cannot be empty')
        elif not new_password:
            flash('New Password cannot be empty')

    return render_template('profile.html', current_user=current_user, cache_id=cache_id)


@app_views_auth.route('/logout', methods=['GET'])
def logout():
     logout_user()
     return redirect(url_for('app_views_main.index'))
