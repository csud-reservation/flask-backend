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

from flask import copy_current_request_context
from gevent import spawn

@main.route('/')
def index():
    if ('userID' in session):
        message = 'Ravis de vous revoir, ' + session['first_name'] + ' ' + session['last_name'] + ' !'
    else:
        message = 'Veuillez vous connecter pour accéder à toutes les fonctionnalités de cette application'
    return render_template('index.html', message=message)

@main.route('/sql', methods=['GET', 'POST'])
def sql():
    if ('userID' in session):
        query = "SELECT * FROM users LIMIT 10;"
        # result = db.session.execute(query)
        return render_template('sql.html', sql=query)
    else:
        return redirect(url_for('main.login')+'?please_login')
    
@main.route('/search', methods=['GET'])
def search_page():
    if ('userID' in session):
        return render_template('search.html')
    else:
        return redirect(url_for('main.login')+'?please_login')
    
@main.route('/login', methods=['GET', 'POST'])
def login():
    # http://flask.pocoo.org/docs/0.12/api/#flask.copy_current_request_context
    # @copy_current_request_context
    # def s(): session.permanent = True
    # spawn(s)  
    
    if (request.method == 'GET'):
        return render_template('login.html')
    if (request.method == 'POST'):
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
            userID = str(result['id'])
            if (password == true_password):
                # enregistrement de la session
                session['first_name'] = first_name
                session['last_name'] = last_name
                session['userID'] = userID
                return 'successfuly logged in'
            else:
                return 'login error' # faux mot de passe
        except TypeError:
            return 'login error' # utilisateur introuvable

@main.route('/logout', methods=['GET', 'POST'])
def logout(): 
    for element in ['userID', 'first_name', 'last_name']:
        session.pop(element, None)
    return redirect(url_for('main.login')+'?just_logged_out')

@main.route('/user/<int:userID>', methods=['GET', 'POST'])
def profil(userID):
    if ('userID' in session):
        query = select(['*']).where(User.id == userID)
        result = db.session.execute(query).first()
        return render_template('profil.html', infos=result)
    else:
        return redirect(url_for('main.login')+'?please_login')