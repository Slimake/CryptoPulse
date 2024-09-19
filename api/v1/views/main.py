#!/usr/bin/python3

from models import storage
from models.user import User
from api.v1.views import app_views_main
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user, login_user
from uuid import uuid4
import bcrypt


@app_views_main.route('/')
def index():
    """Homepage"""
    cache_id = uuid4() # generate random uuid
    return render_template('homepage.html', cache_id=cache_id)


@app_views_main.route('/market')
def market():
    """Market"""
    cache_id = uuid4() # generate random uuid
    return render_template('market.html', cache_id=cache_id)

@app_views_main.route('/news')
def news():
    """News"""
    cache_id = uuid4() # generate random uuid
    return render_template('news.html', cache_id=cache_id)

@app_views_main.route('/prediction')
def prediction():
    """Prediction"""
    cache_id = uuid4() # generate random uuid
    return render_template('prediction.html', cache_id=cache_id)
