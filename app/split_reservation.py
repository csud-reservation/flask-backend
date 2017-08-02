from . import db
from .queries import *
from .models import *

from datetime import timedelta, date, datetime
from flask.ext.login import current_user


def split_reservation_by_student_group(start_date, end_date, first_period, last_period, student_group):
    
        weekday_id = start_date.weekday()+1
        
        res_to_split = search_reservations_by_student_group(start_date, end_date, student_group, weekday_id, first_period, last_period)
    
        number_of_weeks = (end_date - start_date)//7
        number_of_weeks = number_of_weeks.days+1
        
        weeks_to_add = timedelta(weeks=number_of_weeks)
        one_week = timedelta(weeks=1)

        for res in res_to_split:

            user_id = db.engine.execute("SELECT reservations_users.user_id  from reservations  LEFT JOIN reservations_users ON reservations.id = reservations_users.reservation_id  WHERE id=?", [res.reservation_id])
            
            user_id_tuple=()
            for u in user_id:
                user_id_tuple = user_id_tuple + (u[0],)
            print(user_id_tuple)
            
            user = User.query.filter(User.id.in_(user_id_tuple))
            print(user.all())
            
            
            timeslots = Timeslot.query.filter(
            Timeslot.order.between(
                res.timeslot_id-1,
                res.timeslot_id-1,
            )
            ).all()
            
            try:
                old_end_date = datetime.strptime(res.end_date, "%Y-%m-%d")
            except:
                old_end_date = datetime.strptime(res.end_date, "%Y-%m-%d %H:%M:%S")
            
            #Création de la nouvelle réservation avec une date de début correspondant à la date de fin de la suppression
            reservation = Reservation(
                start_date=start_date+weeks_to_add,
                end_date=old_end_date,
                reason_short=res.reason_short,
                reason_details=res.reason_details,
                duration=res.duration,
                student_group=res.student_group,
                users=user,
                room_id=res.room_id,
                timeslots=timeslots,
                weekday_id=weekday_id,
                owner_id=current_user.id

            )
            db.session.add(reservation)
            
            
        db.session.commit()
        
        #Modification de l'ancienne réservation pour que la date de fin corresponde à la date du début de la suppression
        update_reservations_by_student_group(start_date, end_date, student_group, weekday_id, first_period, last_period)
        db.session.commit()
    

def split_reservation_by_room(start_date, end_date, first_period, last_period, room):
    
        weekday_id = start_date.weekday()+1
        
        res_to_split = search_reservations_by_room(start_date, end_date, room, weekday_id, first_period, last_period)
    
        number_of_weeks = (end_date - start_date)//7
        number_of_weeks = number_of_weeks.days+1
        
        weeks_to_add = timedelta(weeks=number_of_weeks)
        one_week = timedelta(weeks=1)

        for res in res_to_split:
            #print(res)

            user_id = db.engine.execute("SELECT reservations_users.user_id  from reservations  LEFT JOIN reservations_users ON reservations.id = reservations_users.reservation_id  WHERE id=?", [res.reservation_id])
            
            user_id_tuple=()
            for u in user_id:
                user_id_tuple = user_id_tuple + (u[0],)
            
            user = User.query.filter(User.id.in_(user_id_tuple))
            #print(user.all())
            
            
            timeslots = Timeslot.query.filter(
            Timeslot.order.between(
                res.timeslot_id-1,
                res.timeslot_id-1,
            )
            ).all()
            
            
            
            try:
                old_end_date = datetime.strptime(res.end_date, "%Y-%m-%d")
            except:
                old_end_date = datetime.strptime(res.end_date, "%Y-%m-%d %H:%M:%S")
            
            #Création de la nouvelle réservation avec une date de début correspondant à la date de fin de la suppression
            reservation = Reservation(
                start_date=start_date+weeks_to_add,
                end_date=old_end_date,
                reason_short=res.reason_short,
                reason_details=res.reason_details,
                duration=res.duration,
                student_group=res.student_group,
                users=user,
                room_id=res.room_id,
                timeslots=timeslots,
                weekday_id=weekday_id,
                owner_id=res.owner_id

            )
            db.session.add(reservation)
            
            
        db.session.commit()
        
        #Modification de l'ancienne réservation pour que la date de fin corresponde à la date du début de la suppression
        update_reservations_by_room(start_date, end_date, room, weekday_id, first_period, last_period)
        db.session.commit()
        
        return res_to_split
        
        
        
def split_reservation_by_id(date, reservation_id):
    
        res = Reservation.query.filter_by(id=reservation_id).first()
        one_week = timedelta(weeks=1)

        user_id = db.engine.execute("SELECT reservations_users.user_id  from reservations  LEFT JOIN reservations_users ON reservations.id = reservations_users.reservation_id  WHERE id=?", [reservation_id])
        
        user_id_tuple=()
        for u in user_id:
            user_id_tuple = user_id_tuple + (u[0],)
        print(user_id_tuple)
        
        user = User.query.filter(User.id.in_(user_id_tuple))
        print(user.all())
        
        
        # timeslots = Timeslot.query.filter(
        # Timeslot.order.between(
        #     res.timeslot_id-1,
        #     res.timeslot_id-1,
        # )
        # ).all()
        
        try:
            old_end_date = datetime.strptime(str(res.end_date), "%Y-%m-%d")
        except:
            old_end_date = datetime.strptime(str(res.end_date), "%Y-%m-%d %H:%M:%S")
            
        date = datetime.strptime(date, "%d.%m.%Y")
        
        weekday_id = date.weekday()+1
        
        #Création de la nouvelle réservation avec une date de début correspondant à la date de fin de la suppression

        if date+one_week < old_end_date:
            reservation = Reservation(
                start_date=date+one_week,
                end_date=old_end_date,
                reason_short=res.reason_short,
                reason_details=res.reason_details,
                duration=res.duration,
                student_group=res.student_group,
                users=user,
                room_id=res.room_id,
                timeslots=res.timeslots,
                weekday_id=weekday_id,
                owner_id=res.owner_id
    
            )
            db.session.add(reservation)
            
            db.session.commit()
                
        #Modification de l'ancienne réservation pour que la date de fin corresponde à la date du début de la suppression
        
            print(reservation_id)
            db.engine.execute('UPDATE reservations SET end_date = ? WHERE id = ?', [date-one_week, reservation_id])
            
            db.session.commit()
            
        else:
            db.engine.execute('DELETE FROM reservations WHERE reservations.id = ? ', reservation_id)
            db.engine.execute('DELETE FROM reservations_users WHERE reservation_id = ?', reservation_id)
            db.engine.execute('DELETE FROM reservations_timeslots WHERE reservation_id = ?', reservation_id)
    
        
def get_reservation_by_room(start_date, end_date, first_period, last_period, room):
    
    weekday_id = start_date.weekday()+1
    return search_reservations_by_room(start_date, end_date, room, weekday_id, first_period, last_period)
    