#!/usr/bin/python3
"""Blueprint for API"""
from flask import Blueprint

app_views_main = Blueprint('app_views_main', __name__, url_prefix='/')
app_views_auth = Blueprint('app_views_auth', __name__, url_prefix='/')

from api.v1.views.main import *
from api.v1.views.auth import *
