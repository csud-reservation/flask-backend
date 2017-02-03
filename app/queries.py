from . import db

def search_query(weekday_id, first_period, last_period, current_date, room_type):
    '''
    Retourne toutes les salles disponibles à la date donnée
    '''
    
    
    data = [weekday_id, first_period, last_period, current_date, current_date, room_type]
    #print (data)
    
    result = db.engine.execute(
        ''' SELECT rooms.name 
            FROM rooms
            WHERE rooms.id NOT IN
                (SELECT rooms.id
                FROM rooms
                LEFT JOIN reservations ON reservations.room_id = rooms.id
                LEFT JOIN reservations_timeslots ON reservations.id = reservations_timeslots.reservation_id
                WHERE reservations.weekday_id = ?
                    AND reservations_timeslots.timeslot_id BETWEEN ? AND ?
                    AND reservations.start_date <= ?
                    AND reservations.end_date >= ?)
            AND rooms.name LIKE ?;
            ''', data)
    
    return result
    
def my_reservations(user_id):
    
    result = db.engine.execute(
    ''' SELECT reservations.* 
        FROM reservations
        WHERE reservations.owner_id = ?;
        ''', user_id)
    return result
    
    