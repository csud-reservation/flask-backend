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
from sqlalchemy import func, text, desc
import re

from werkzeug.security import generate_password_hash, check_password_hash


from flask import copy_current_request_context

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from ..forms import LoginForm, ChangePasswordForm
from ..queries import *

from datetime import timedelta, date, datetime

def test_regex(regex, to_test):
    pattern = re.compile("^.+$")
    return pattern.match(to_test)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/timetable_ajax', methods=['POST'])
def timetable():
    start_date_str = datetime.strptime(request.args.get('start_date'), "%d.%m.%Y")
    start_date = start_date_str.date()
    end_date_str = datetime.strptime(request.args.get('end_date'), "%d.%m.%Y")
    end_date = start_date_str.date()
    
    timetable = weekly_timetable(request.args.get('room_number'), start_date, end_date)
    timeslots = Timeslot.query.all()
    room = request.args.get('room_number')
    days = Weekday.query.limit(5).all()
    return render_template(
        'timetable.html',
        room=room, 
        timetable=timetable, 
        days=days, 
        timeslots=timeslots
    )

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    if (request.method == 'POST'):
        
        session['start_date'] = datetime.strptime(request.form.get('start_date'), "%d.%m.%Y")
        session['end_date'] = datetime.strptime(request.form.get('end_date'), "%d.%m.%Y")
        
        session['weekday_id'] = session['start_date'].weekday()+1
        session['first_period'] = int(request.form.get('firstID')) + 1
        session['last_period'] = int(request.form.get('lastID')) + 1
        session['room_type'] = request.form.get('room_type')

        number_of_weeks = (session['end_date'] - session['start_date'])//7
        number_of_weeks = number_of_weeks.days+1

        current_date = session['start_date']
        a_week = timedelta(weeks = 1)
        
        disponibilities = {}
        #print (number_of_weeks)
        for w in range(number_of_weeks):

            result = search_query(session['weekday_id'], session['first_period'], session['last_period'], current_date.date(), session['room_type'])
            current_date = current_date + a_week
            
            for rooms in result:
                #print("rooms", rooms)
                if not rooms['name'] in disponibilities.keys() :
                    disponibilities[rooms['name']] = 1
                else :
                    disponibilities[rooms[0]] = disponibilities[rooms[0]] + 1
            #print (disponibilities)
            
        #Supprimer les salles qui ne sont pas disponibles toutes les semaines
        #TODO : modifier pour que l'admin puisse y accéder aux salles avec conflit et les écraser
        keys_with_conflict = []
        for key, value in disponibilities.items():
    
            if value < number_of_weeks :
                print ("key : ",key)
                keys_with_conflict.append(key)
                
        for e in keys_with_conflict:
            del disponibilities[e]
        
        #Retourne une page spéciale si il n'y a pas de résultat satisfaisant
        if not bool(disponibilities) :
            return render_template('search_empty.html')
            
        return render_template('search_results.html',
            disponibilities=disponibilities,
            start_date=session['start_date'].date(),
            end_date=session['end_date'].date(),
            first_period = session['first_period'],
            last_period = session['last_period']
        )

    else:
        return render_template('search.html')
        
#===============================================================================
        
@main.route('/search_confirm', methods=['POST'])
@login_required
def search_confirm():
    ''' 
    Effectue la réservation pour de vrai
    '''
    
    room_select = request.form.get('room_select')
    student_group = request.form.get('student_group')
    reason = request.form.get('reason')
    
    duration = session['last_period'] - session['first_period'] + 1
    
    user = User.query.get(current_user.id)
    timeslots = Timeslot.query.filter(
        Timeslot.order.between(
            session['first_period'],
            session['last_period'],
        )
    ).all()
    weekday = Weekday.query.get(session['weekday_id'])
    room = Room.query.filter_by(name=room_select).first()
    
    reservation = Reservation(
        # dates du début et de fin d'année
        start_date=session['start_date'],
        end_date=session['end_date'],
        reason_details=reason,
        duration=duration,
        student_group=student_group,
        users=[user],
        room=room,
        timeslots=timeslots,
        weekday=weekday,
        owner=user
    )
        
    db.session.add(reservation)
    db.session.commit()
    
    return render_template('search_confirm.html')
   
   
#======================================================================================
# LOGIN
#======================================================================================

@main.route('/login')
def login():
    loginForm = LoginForm()
    #wrongCombinationAP permet d'envoyer au client si la combinaison Account-Password est correcte ou non
    session['wrongCombinationAP'] = False
    if loginForm.validate_on_submit():
        
        if '@' in loginForm.account.data :
            user = User.query.filter(
                func.lower(User.email) == func.lower(loginForm.account.data)
            ).first()
        else: #Alors il s'agit du sigle
            user = User.query.filter_by(
                sigle=loginForm.account.data.upper()
            ).first()
        
        if user is None or not user.verify_password(loginForm.password.data):
            session['wrongCombinationAP'] = True
            return render_template('login.html',
                form=loginForm,
                wrongCombination=session['wrongCombinationAP']
            )
        session['wrongCombinationAP'] = False
        login_user(user, loginForm.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.search_page'))
        
    return render_template('login.html',
        form=loginForm,
        wrongCombination=session['wrongCombinationAP']
    )

#============================================================================
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#============================================================================
@main.route('/user')
@login_required
def profil():
    
    # CombinationPP (pour Combinaison Password-Password) permet d'envoyer au client le type d'erreur dans le changement de mot de passe
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
        return render_template('profil.html',
            infos=result,
            form=changePWForm,
            combination=session['CombinationPP']
        )

    session['CombinationPP'] = 0 
    return render_template('profil.html',
        infos=result,
        form=changePWForm,
        combination=session['CombinationPP']
    )
    
@main.route('/timetable')
@login_required
def horaire():
    rooms = Room.query.all()
    return render_template('horaire.html', rooms=rooms)
    
@main.route('/mes_reservations')
@login_required
def mes_reservations():
    reservations = Reservation.query.filter_by(owner_id=current_user.id).all()
    # result = my_reservations(current_user.id)
    return render_template('mes_reservations.html',
        reservations=reservations
    )