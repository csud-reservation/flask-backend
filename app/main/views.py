# fonction de débug pour imprimer quelque chose dans la console flask
from __future__ import print_function
import sys
def print_to_console(toprint):
    print(toprint, file=sys.stderr)

from flask import render_template, session, redirect, url_for, current_app, request, g
from .. import db
from ..models import *
from ..email import send_email
from . import main
from sqlalchemy.sql import select
from sqlalchemy import func, text



from werkzeug.security import generate_password_hash, check_password_hash


from flask import copy_current_request_context
from gevent import spawn
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from ..forms import LoginForm, ChangePasswordForm

from datetime import timedelta, date, datetime


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search', methods=['GET'])
#@login_required
def search_page():
    
    #@SAMUEL : Là c'est toutes les variables "placeholder" que j'ai mises jusqu'à maintenant.
    #Il faudrait les remplacer avec les vraies valeurs du formulaire !
    
    start_date = datetime.strptime("02/02/2017", "%d/%m/%Y")
    end_date = datetime.strptime("16/02/2017", "%d/%m/%Y")
    week_id = 1
    first_period = 1
    last_period = 1
    room_type = "(PHL)"
    
    
    number_of_weeks = (end_date - start_date)//7
    number_of_weeks = number_of_weeks.days+1
    
    current_date = start_date
    a_week = timedelta(weeks = 1)
    
    
    disponibilities = {}
    for w in range(number_of_weeks):
        
        current_date = current_date + a_week
        #print(current_date.date())

        sql = text('''SELECT rooms.name 
                    FROM rooms
                    WHERE rooms.id NOT IN
                        (SELECT rooms.id
                        FROM rooms
                        LEFT JOIN reservations ON reservations.room_id = rooms.id
                        LEFT JOIN reservations_timeslots ON reservations.id = reservations_timeslots.reservation_id
                        WHERE reservations.weekday_id = {week_id}
                            AND reservations_timeslots.timeslot_id BETWEEN {first_period} AND {last_period}
                            AND reservations.start_date < "{start_date}"
                            AND reservations.end_date > "{end_date}")
                    AND rooms.name LIKE "%{room_type}";
                            '''.format(week_id = week_id, first_period=first_period, last_period=last_period, start_date = current_date.date(), end_date = current_date.date(), room_type=room_type ))
        
                            
        result = db.engine.execute(sql)
        rooms = []
        for row in result:
            if not row[0] in disponibilities.keys() :
                disponibilities[row[0]] = 0
            else :
                disponibilities[row[0]] = disponibilities[row[0]] + 1
                
    for keys,values in disponibilities.items():
        print (keys, values)


    return render_template('search.html', rooms=rooms)
   
#========================================================================================================================================================
#=====LOGIN==============================================================================================================================================
#========================================================================================================================================================

@main.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    session['wrongCombinationAP'] = False
    if loginForm.validate_on_submit():
        
        if '@' in loginForm.account.data :
            user = User.query.filter_by(email=loginForm.account.data).first()
        else: #Alors il s'agit du sigle
            user = User.query.filter_by(sigle=loginForm.account.data.upper()).first()

        
        if user is None or not user.verify_password(loginForm.password.data):
            session['wrongCombinationAP'] = True
            return render_template('login.html', form=loginForm, wrongCombination=session['wrongCombinationAP'])
        session['wrongCombinationAP'] = False
        login_user(user, loginForm.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.search_page'))
    return render_template('login.html', form=loginForm, wrongCombination=session['wrongCombinationAP'])

#========================================================================================================================================================

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#========================================================================================================================================================

@main.route('/user', methods=['GET', 'POST'])
@login_required
def profil():
    session['CombinationPP'] = 0
    changePWForm = ChangePasswordForm()
    query = select(['*']).where(User.id == current_user.id)
    result = db.session.execute(query).first()
    
    if changePWForm.validate_on_submit():
        
        
        if not current_user.verify_password(changePWForm.old_pw.data):
            session["CombinationPP"] = 2
            
        elif not changePWForm.new_pw.data == changePWForm.new_pw2.data:
            session["CombinationPP"] = 3
            
        else:
            session["CombinationPP"] = 1
            current_user.password_hash = generate_password_hash(changePWForm.new_pw2.data)
            db.session.commit()
        return render_template('profil.html', infos=result, form=changePWForm, combination=session['CombinationPP'])
        
            

            
            
    session['CombinationPP'] = 0 
    return render_template('profil.html', infos=result, form=changePWForm, combination=session['CombinationPP'])