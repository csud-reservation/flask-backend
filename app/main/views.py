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
from flask_mail import Message

from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from ..forms import LoginForm, ChangePasswordForm
from ..queries import *
from ..split_reservation import *

from datetime import timedelta, date, datetime

def get_roles_list():
    roles = Role.query.all()
    roles_list = ['']
    for role in roles:
        roles_list.append(role.description)
    return roles_list

def get_student_groups_list():
    s = db.session.query(Reservation.student_group).distinct()
    student_groups_list = []
    for sg in s :
        if sg[0].strip("[]"):
            student_groups_list.append(sg[0].strip("[]"))
    return sorted(student_groups_list)
    
def get_rooms_list():
    all_rooms = db.engine.execute("SELECT rooms.name FROM rooms")
    room_list = []
    for r in all_rooms :
        room_list.append(r[0])
    return sorted(room_list)
    
    
def get_all_rooms_with_conflicts(start_date, end_date, first_period, last_period, room_type):
    
    weekday_id = start_date.weekday()+1
    number_of_weeks = (end_date - start_date)//7
    number_of_weeks = number_of_weeks.days+1

    current_date = start_date
    one_week = timedelta(weeks = 1)

    all_rooms = db.engine.execute("SELECT rooms.name FROM rooms")
    all_rooms_with_conflicts = {}
    possible_conflicts = (last_period+1-first_period)*number_of_weeks
    
    for rooms in all_rooms:
        all_rooms_with_conflicts[rooms[0]] = possible_conflicts
        
     
    all_rooms_free_at_least_once = []  
    for w in range(number_of_weeks):
        for i in range(last_period-first_period+1):
            free_rooms = search_query(weekday_id, first_period+i+1, first_period+i+1, current_date.date(), room_type)
            for r in free_rooms:
                all_rooms_free_at_least_once.append(r[0])
        current_date = current_date + one_week

    
    for r in all_rooms_free_at_least_once:
        all_rooms_with_conflicts[r] = all_rooms_with_conflicts[r]-1
        
    return all_rooms_with_conflicts
    
    


@main.route('/', methods=['GET'])
def index():
    return redirect(url_for('main.profil'))

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    
    if (request.method == 'POST'):
        
        start_date = datetime.strptime(request.form.get('start_date'), "%d.%m.%Y")
        end_date = datetime.strptime(request.form.get('end_date'), "%d.%m.%Y")
        
        first_period = int(request.form.get('firstID'))
        last_period = int(request.form.get('lastID'))
        room_type = request.form.get('room_type')


        all_rooms_with_conflicts = get_all_rooms_with_conflicts(start_date, end_date, first_period, last_period, room_type)
                
        admin_rights = request.form.get('adminRights') == 'true'
        session["admin_rights"] = admin_rights
        
        user_role = Role.query.get(current_user.role_id).name
        
        if admin_rights and user_role == 'admin':
            
            sorted_all_rooms_with_conflicts = sorted(all_rooms_with_conflicts.items(), key=lambda x: (x[1],x[0]))
            
            return render_template('search_results.html',
                disponibilities=sorted_all_rooms_with_conflicts,
                start_date=start_date.date(),
                end_date=end_date.date(),
                first_period = first_period,
                last_period = last_period,
                admin_rights = 1
            )    
        
        else :
            keys_with_conflict = []
            for key, value in all_rooms_with_conflicts.items():
        
                if value > 0 :
                    print ("key : ",key)
                    keys_with_conflict.append(key)
                    
            for e in keys_with_conflict:
                del all_rooms_with_conflicts[e]
            
            #Retourne une page spéciale si il n'y a pas de résultat satisfaisant
            if not bool(all_rooms_with_conflicts) :
                return 'no room available'
                
            return render_template('search_results.html',
                disponibilities=all_rooms_with_conflicts,
                start_date=start_date.date(),
                end_date=end_date.date(),
                first_period = first_period,
                last_period = last_period,
                admin_rights = 0
            )

    user_role = Role.query.get(current_user.role_id).name
    return render_template('search.html', role=user_role)
        
#===============================================================================
     

@main.route('/new_reservation', methods=['PUT', 'POST'])
@login_required
def new_reservation():
    
    room_select = request.form.get('room_select')
    student_group = request.form.get('student_group')
    reason = request.form.get('reason')
    res_name = request.form.get('res_name')
    first_period = int(request.form.get('first_period'))
    last_period = int(request.form.get('last_period'))
    start_date = datetime.strptime(request.form.get('start_date'), "%d.%m.%Y")
    end_date = datetime.strptime(request.form.get('end_date'), "%d.%m.%Y")
    weekday_id = start_date.weekday()+1
    
    
    all_rooms_with_conflicts = get_all_rooms_with_conflicts(start_date, end_date, first_period, last_period, "%%")
    
    session["modifications"] = []
    session["modifications_dates"] = []
    session["old_room"] = room_select

    print(all_rooms_with_conflicts)
    
    user_role = Role.query.get(current_user.role_id).name
    
    if user_role == 'admin' and session["admin_rights"]:
        if all_rooms_with_conflicts[room_select]:
            
            print(all_rooms_with_conflicts[room_select])
            res_to_replace = get_reservation_by_room(start_date, end_date, first_period+1, last_period+1, room_select)

            for res in res_to_replace:

                first_free_room = search_query(weekday_id, res.timeslot_id, res.timeslot_id, start_date.date(), "%%").first()
                
                user_id = db.engine.execute("SELECT reservations_users.user_id  from reservations  LEFT JOIN reservations_users ON reservations.id = reservations_users.reservation_id  WHERE id=?", [res.reservation_id])
            
                user_id_tuple=()
                for u in user_id:
                    user_id_tuple = user_id_tuple + (u[0],)
                
                user = User.query.filter(User.id.in_(user_id_tuple))
                
                timeslots = Timeslot.query.filter(
                Timeslot.order.between(
                    res.timeslot_id-1,
                    res.timeslot_id-1,
                )
                ).all()
                
                room = Room.query.filter_by(name=first_free_room[0]).first()
                
            
                reservation = Reservation(
                start_date=start_date,
                end_date=end_date,
                reason_short=res.reason_short,
                reason_details=res.reason_details,
                duration=res.duration,
                student_group=res.student_group,
                users=user,
                room_id=room.id,
                timeslots=timeslots,
                weekday_id=weekday_id,
                owner_id=current_user.id

                )
                db.session.add(reservation)
                

                session["modifications"].append([res.reason_details, user[0].first_name, user[0].last_name, first_free_room[0]])
                print("new room : ", first_free_room)
                
                old_room_name = Room.query.filter_by(id=res.room_id).first().name
                
                
            db.session.commit()

            res_to_replace.close()
            split_reservation_by_room(start_date, end_date, first_period+1, last_period+1, room_select)
            
    elif not session["admin_rights"]:
        
        print("debug")
        
        if all_rooms_with_conflicts[room_select] > 0:
            
            return "La salle demandée n'est plus disponible"
    
    
    session["modifications_dates"] = [start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')]
    
    duration = last_period - first_period + 1
    
    user = User.query.get(current_user.id)
    timeslots = Timeslot.query.filter(
        Timeslot.order.between(
            first_period,
            last_period,
        )
    ).all()
    weekday = Weekday.query.get(start_date.weekday()+1)
    room = Room.query.filter_by(name=room_select).first()
    
    reservation = Reservation(
        start_date=start_date,
        end_date=end_date,
        reason_short=res_name,
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
    
    # réservation en ajax
    if (request.method == 'PUT'):
        return 'success'

    session['just_reserved'] = True
    # réservation par une requête POST
    return redirect(url_for('main.my_reservations'))
   
   
#======================================================================================
# LOGIN
#======================================================================================

@main.route('/login', methods=['GET', 'POST'])
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
@main.route('/user', methods=['GET', 'PATCH', 'POST', 'PUT', 'DELETE'])
@login_required
def profil():
    user_role = Role.query.get(current_user.role_id).name

    if (request.method == 'PATCH'):
        # s'il n'y pas de rôle dans la requête, ça veut dire qu'elle est faite depuis la page de profil
        if (request.form.get('role') is None):
            role_id = current_user.role_id
            
            if (int(request.form.get('id')) != current_user.id):
                return 'operation interdite'
        else:
            role_id = request.form.get('role')
            
            if (user_role != 'admin'):
                return 'operation interdite'
            
        db.engine.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, sigle = ?, role_id = ? WHERE users.id = ?',
            request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'), 
            request.form.get('sigle').upper(), role_id, request.form.get('id'))

        return 'success'
    
    if (request.method == 'PUT'):
            
        if (user_role != 'admin'):
            return 'operation interdite'
            
        password = password_generator()
        password_hash = generate_password_hash(password)
            
        db.engine.execute('INSERT INTO users(first_name, last_name, email, sigle, role_id, password_hash) VALUES (?,?,?,?,?,?)',
            request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'), 
            request.form.get('sigle').upper(), request.form.get('role'), password_hash)

        return password

    if (request.method == 'DELETE'):
            
        if (user_role != 'admin'):
            return 'operation interdite'
            
        db.engine.execute('DELETE FROM users WHERE id = ?', request.form.get('user_id'))
        return 'success'

    if (request.args.get('sigle') is not None):
        user_id = db.session.execute(select(['id']).where(User.sigle == request.args.get('sigle').upper())).first().id

        if (user_id == current_user.id):
            return redirect(url_for('main.profil'))

        query = select(['*']).where(User.id == user_id)
        result = db.session.execute(query).first()

        return render_template('profil.html', infos=result, role=user_role, roles_list=get_roles_list())

    # CombinationPP (pour Combinaison Password-Password) permet d'envoyer au client le type d'erreur dans le changement de mot de passe
    session['CombinationPP'] = 0
    changePWForm = ChangePasswordForm()
    query = select(['*']).where(User.id == current_user.id)
    result = db.session.execute(query).first()
    
    if changePWForm.validate_on_submit():
        if not current_user.verify_password(changePWForm.old_pw.data):
            session["CombinationPP"] = 2

            return render_template('profil.html',
                role=user_role,
                infos=result,
                form=changePWForm,
                combination=session['CombinationPP'],
                new_password=changePWForm.new_pw2.data)   
        else:
            session["CombinationPP"] = 1
            current_user.password_hash = generate_password_hash(changePWForm.new_pw.data)
            db.session.commit()

    else:
        session['CombinationPP'] = 0 

    return render_template('profil.html',
        role=user_role,
        infos=result,
        form=changePWForm,
        roles_list=get_roles_list(),
        combination=session['CombinationPP'])
    
@main.route('/timetable')
@login_required
def horaire():
    user_role = Role.query.get(current_user.role_id).name
    rooms = Room.query.all()
    user = db.session.execute(select(['*']).where(User.id == current_user.id)).first()
    return render_template('horaire.html', rooms=rooms, user=user, role=user_role)

@main.route('/timetable_ajax', methods=['GET'])
@login_required
def timetable():
    start_date_str = datetime.strptime(request.args.get('start_date'), "%d.%m.%Y")
    start_date = start_date_str.date()
    end_date_str = datetime.strptime(request.args.get('end_date'), "%d.%m.%Y")
    end_date = end_date_str.date()
    
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
    
@main.route('/my_reservations', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def my_reservations():
    
    if (request.method == 'DELETE'):
        db.engine.execute('DELETE FROM reservations WHERE reservations.id = ? ', request.form.get('id'))
        db.engine.execute('DELETE FROM reservations_users WHERE reservation_id = ?', request.form.get('id'))
        db.engine.execute('DELETE FROM reservations_timeslots WHERE reservation_id = ?', request.form.get('id'))

        return 'success'

    if (request.method == 'PATCH'):
        db.engine.execute('UPDATE reservations SET reason_short = ?, reason_details = ?, student_group = ? WHERE reservations.id = ?',
            request.form.get('reason_short'), request.form.get('reason_details'), request.form.get('student_group'), request.form.get('id'))

        return 'success'

    today = datetime.today().date()
    reservations = Reservation.query.filter_by(owner_id=current_user.id).order_by(desc(Reservation.start_date)).limit(50) # à gérer : mettre sur plusieurs pages
    user_role = Role.query.get(current_user.role_id).name
    
    if not 'just_reserved' in session:
        session['just_reserved'] = False
        
    if (session['just_reserved']):
        just_reserved = True
        session['just_reserved'] = False
    else:
        just_reserved = False
        
    if not 'modifications' in session:
        session["modifications"] = []
        session["modifications_dates"] = []
        session["old_room"] = ""
        
    return render_template('my_reservations.html',
        reservations=reservations, today=today, just_reserved=just_reserved, role=user_role, modifications = session["modifications"], modifications_dates = session["modifications_dates"], old_room = session["old_room"])
        
@main.route('/users_admin', methods=['GET'])
@login_required
def users_admin():
    user_role = Role.query.get(current_user.role_id).name
    if user_role != 'admin':
        return 'acces interdit'
    
    users = User.query.order_by('sigle').all()
    return render_template('users_admin.html', users=users, roles=get_roles_list(), role=user_role)
    
@main.route('/last_user', methods=['GET'])
@login_required
def last_user():
    user = User.query.order_by('-id').first()
    return render_template('last_user.html', user=user, roles=get_roles_list())
    
@main.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    user_role = Role.query.get(current_user.role_id).name
    if user_role != 'admin':
        return 'acces interdit'
    
    password = password_generator()
    password_hash = generate_password_hash(password)
    
    db.engine.execute('UPDATE users SET password_hash = ? WHERE users.id = ?',
    password_hash, request.form.get('user_id'))
    
    return password
    
    
@main.route('/freegroup', methods=['GET',"POST", "PATCH"])
@login_required
def freegroup():
    user_role = Role.query.get(current_user.role_id).name
    if user_role != 'admin':
        return 'acces interdit'
        
        
    if request.method == 'PATCH':
        

        start_date = datetime.strptime(request.form.get('start_date'), "%d.%m.%Y")
        end_date = datetime.strptime(request.form.get('end_date'), "%d.%m.%Y")
        first_period = int(request.form.get('firstID'))+1
        last_period = int(request.form.get('lastID'))+1
        weekday_id = start_date.weekday()+1
        
        if request.form.get("type") == "student_group":
            split_reservation_by_student_group(start_date, end_date, first_period, last_period, request.form.get("group"))
        
        else:
            split_reservation_by_room(start_date, end_date, first_period, last_period, request.form.get("group"))



    user_role = Role.query.get(current_user.role_id).name
    return render_template('freeGroup.html', role = user_role, student_groups = get_student_groups_list(), rooms = get_rooms_list())
    
