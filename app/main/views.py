# fonction de débug pour imprimer quelque chose dans la console flask
from __future__ import print_function
import sys
def print_to_console(toprint):
    print(toprint, file=sys.stderr)

from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from sqlalchemy.sql import select
from sqlalchemy import func

@main.route('/')
def index():
    return render_template('index.html', message="Ravis de vous revoir")

@main.route('/sql', methods=['GET', 'POST'])
def sql():
    query = "SELECT * FROM users LIMIT 10;"
    #result = db.session.execute(query)
    return render_template('sql.html', sql=query)
    
@main.route('/login', methods=['GET'])
def login_show():
    return render_template('login.html')
    
@main.route('/login', methods=['POST'])
def login_control():
    user = request.args.get('user').lower()
    password = request.args.get('password')
    if ('@' in user):
        query = select(['*']).where(func.lower(User.email) == user)
    else:
        query = select(['*']).where(func.lower(User.sigle) == user)
    try:
        result = db.session.execute(query).first()
        true_password = result['password_hash']
        first_name, last_name = result['first_name'], result['last_name']
        if (password == true_password):
            return 'bonjour, ' + first_name + ' ' + last_name + ' !'
        else:
            return 'mot de passe erroné'
    except:
        return 'utilisateur introuvable'