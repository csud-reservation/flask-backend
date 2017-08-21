from . import db

from .models import Timeslot, Weekday

from sqlalchemy.sql import text

def search_query(weekday_id, first_period, last_period, current_date, room_type):
    '''
    Retourne toutes les salles disponibles à la date donnée
    '''
    
    # la réservation récurrente ne fonctionne pas, puisque nous utilisons deux fois "current_date"
    data = [weekday_id, first_period, last_period, current_date, current_date, room_type]
    #print (data)

    
    result = db.engine.execute(
        ''' SELECT rooms.name 
            FROM rooms
            WHERE rooms.id NOT IN
                (SELECT rooms.id
                FROM rooms
                LEFT JOIN reservations
                    ON reservations.room_id = rooms.id
                LEFT JOIN reservations_timeslots
                    ON reservations.id = reservations_timeslots.reservation_id
                WHERE reservations.weekday_id = ?
                    AND reservations_timeslots.timeslot_id BETWEEN ? AND ?
                    AND reservations.start_date <= ?
                    AND reservations.end_date >= ?)
            AND rooms.name LIKE ?;
            ''', data)
    
    return result
    

def weekly_timetable(room_number, week_start_date, week_end_date):
    '''
    Retourne la liste de tous les timeslots possédant une réservation pour la
    salle ``room_id`` durant la semaine comprenant la date ``day_date``.
    '''

    query = '''
        SELECT
            timeslots.id AS [timeslot_id],
            roles.name AS [owner_role],
            weekdays.id as [weekday_id],
            weekdays.name as [day],
            reservations.reason_short [reason],
            reservations.student_group,
            group_concat(users.sigle, ' - ') AS [users]
        FROM timeslots
            LEFT JOIN reservations_timeslots
                ON reservations_timeslots.timeslot_id = timeslots.id
            LEFT JOIN reservations
                ON reservations.id = reservations_timeslots.reservation_id
            LEFT JOIN users AS owner
                ON reservations.owner_id = owner.id
            LEFT JOIN roles
                ON owner.role_id = roles.id
            LEFT JOIN rooms
                ON reservations.room_id = rooms.id
            LEFT JOIN reservations_users
                ON reservations_users.reservation_id = reservations.id
            LEFT JOIN users
                ON reservations_users.user_id = users.id
            LEFT JOIN weekdays
                ON reservations.weekday_id = weekdays.id
        WHERE 
            rooms.name = ?
        AND NOT (
            reservations.start_date > ? OR reservations.end_date < ?
        )
        GROUP BY timeslots.id, weekdays.id
        ORDER BY weekdays.id, timeslots.id;
        '''
        
    week_reservation = db.engine.execute(query, [
        room_number,
        week_end_date, week_start_date
    ])
    
    weekdays = Weekday.query.all()
    timeslots = Timeslot.query.all()

    # Pour chaque plage horaire existante
    timetable_rows = [None] * len(timeslots)
    for i, ts in enumerate(timeslots):
        timetable_rows[i] = [None] * len(weekdays)

    for row in week_reservation:
        timeslot_id = row['timeslot_id']
        weekday_id = row['weekday_id']
        timetable_rows[timeslot_id-1][weekday_id-1] = row

    return timetable_rows
