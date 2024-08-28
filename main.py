from flask import Blueprint, render_template, redirect, url_for, session, request, flash, abort

from .model import Model
from .crpt import Crypt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #return render_template('signup.html')
    return redirect(url_for('main.login'))
    #return render_template('login.html')

@main.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    if user == 'admin' and password == 'password':
            return f'Welcome, {user}!'
        else:
            return 'Invalid username or password!', 401

    return render_template('login.html', error=error)

@main.route('/signup', methods=['POST', 'GET'])
def signup():
     error = None
     if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')
          confirm_password = request.form.get('confirm_password')
          
          #Validation check
          if confirm_password != password:
               error = "Passwords do not match!"
          elif username == 'admin':
               error = "Username already taken!"
          else:
               flash('Succefully signed up! Please log in.')
               return redirect(url_for('main.login'))
    return render_template('signup.html', error=error)

app.register_blueprint(main)     

if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0', port=5000)