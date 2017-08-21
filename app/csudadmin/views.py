from flask import render_template, session, redirect, url_for, current_app, request, g
from .. import db
from ..models import *

from ..email import send_email
from . import csudadmin as admin
from sqlalchemy.sql import select
from sqlalchemy import func, text, desc

from flask import copy_current_request_context

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

'''
'''

@admin.route('/')
def index():
    return render_template('admin_index.html')