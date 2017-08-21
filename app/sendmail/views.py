import os

from flask import render_template, request, url_for
from .. import db
from ..models import *

from . import sendmail

from ..email import send_email

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

    
@sendmail.route('/user')
@login_required
def send_test_mail():
    user = User.query.get(current_user.id)
    my_reservations_url = 'https://' + os.environ.get('C9_HOSTNAME') + url_for('main.my_reservations')
    send_email(
        user.email,
        "Test du système de mails",
        'test',
        user=user,
        my_reservations_url=my_reservations_url
    )
    return "le courriel a bien été envoyé à l'adresse " + user.email + '.' + my_reservations_url
    