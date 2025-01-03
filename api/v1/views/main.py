#!/usr/bin/python3

from models import storage
from models.user import User
from api.v1.views import app_views_main
from flask import render_template
from uuid import uuid4
import os
import requests
import requests_cache


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
    # Enable a cache with SQLite as the backend
    requests_cache.install_cache('http_cache', backend='sqlite', expire_after=1200)

    cache_id = uuid4() # generate random uuid
    url = 'https://newsdata.io/api/1/news?q=crypto'
    api_key = os.getenv('X-ACCESS-KEY')
    headers = {'X-ACCESS-KEY': api_key}

    req = requests.get(url, headers=headers)
    news = req.json()

    return render_template('news.html', news=news, cache_id=cache_id)

@app_views_main.route('/prediction')
def prediction():
    """Prediction"""
    cache_id = uuid4() # generate random uuid
    return render_template('prediction.html', cache_id=cache_id)

@app_views_main.route('/about')
def about():
    """About"""
    cache_id = uuid4() # generate random uuid
    return render_template('about.html', cache_id=cache_id)
