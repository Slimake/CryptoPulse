from flask import Blueprint, render_template, redirect, url_for, session, request, flash, abort

import bcrypt
from models.engine.db_storage import DBStorage
from models.user import User

#Initializing DBStorage
storage = DBStorage()
storage.reload()

app = Flask(__name__)
app.secret_key = 'secret_key'

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #return render_template('login.html')
    return redirect(url_for('main.login'))


@main.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'] #Ask the guys if we want to use email or username to login
        password = request.form['password']

    
    # Fetch user data from database
    user = storage.get_user_by_username(username)

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
         session['user_id'] = user.id #query: set session variable
         flash('Successfully logged in!', 'Success')
         return f'Welcome, {user.username}!'
    else:
         error = 'Invalid username or password!'

    return render_template('login.html', error=error)

@main.route('/signup', methods=['POST', 'GET'])
def signup():
     error = None
     if request.method == 'POST':
          email = request.form.get('email')
          username = request.form.get('username')
          password = request.form.get('password')
          confirm_password = request.form.get('confirm_password')
          
          #Validation check
          if confirm_password != password:
               error = "Passwords do not match!"
          elif storage.get_user_by_username(username):
               error = "Username already taken!"
          else:
               password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
               new_user = User(email=email, username=username, password_hash=password_hash)

               #Saving new_user to DBStorage
               storage.add(new_user)

               flash('Succefully signed up! Please log in.')
               return redirect(url_for('main.login'))
          
          return render_template('signup.html', error=error)

app.register_blueprint(main)     

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)