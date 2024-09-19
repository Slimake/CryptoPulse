#!/usr/bin/python3
""" Flask Application """
from models import storage
from models.user import User
from api.v1.views import app_views_auth
from api.v1.views import app_views_main
from os import environ
from flask import Flask, render_template, jsonify, make_response, redirect, url_for, session, request, flash, abort
from flask_login import LoginManager
#from flask_cors import CORS
from api.v1.views import *
import os

app = Flask(__name__)
app.register_blueprint(app_views_auth)
app.register_blueprint(app_views_main)
app.secret_key = os.urandom(24) # Generates a 24-byte random key
#cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

login_manager = LoginManager()
login_manager.login_view = 'app_views_auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    # since the id is just the primary key of our user table, use it in the query for the user
    return storage.get_id(User, id)

@app.teardown_appcontext
def close_db(error):
    """Close DBStorage or called the reload method of fileStorage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 Error"""
    return render_template('404.html')

if __name__ == '__main__':
    host = '0.0.0.0'
    port = '5000'

    app.run(debug=True, host=host, port=port)
