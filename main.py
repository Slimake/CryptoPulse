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
        
    return render_template('login.html', error=error)
    #return 'Hello'