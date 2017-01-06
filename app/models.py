from . import db

db.verbosity = 2


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(4), unique=True, index=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(25))
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    # link to roles
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # link to reservations (owner)
    owned_reservations = db.relationship('Reservation', backref='owner')
    # link to reservations (teacher) ==> already done through reser
    
    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    level = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class StudentGroup(db.Model):
    __tablename__ = 'student_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    school_level = db.Column(db.Integer)

    def __repr__(self):
        return '<StudentGroup %r>' % self.name
        
        
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))


    def __repr__(self):
        return '<Room %r>' % self.name


class Timeslot(db.Model):
    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True)
    # Représente le numéro de la page horaire dans un jour donné (nombre entier entre 1 et 10 par exemple)
    no = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    
    # link to reservations ==> already done through reservations_timeslots
    

    def __repr__(self):
        # TODO : il faut encore rajouter le jour auquel cette plage est liée
        return '<Timeslot no=%r>' % self.no



class Weekday(db.Model):
    __tablename__ = 'weekdays'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))
    
    # link to reservations
    reservations = db.relationship('Reservation', backref='weekday')
    

    def __repr__(self):
        # TODO : il faut encore rajouter le jour auquel cette plage est liée
        return '<Weekday id=%r, name=%r>' % (self.id, self.name)

    

## association table from reservations to users (teachers)
reservations_users = db.Table('reservations_users',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservations.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

## association table from reservations to timeslots
reservations_timeslots = db.Table('reservations_timeslots',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservations.id'), primary_key=True),
    db.Column('timeslot_id', db.Integer, db.ForeignKey('timeslots.id'), primary_key=True)
)
    

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reason = db.Column(db.Unicode)
    duration = db.Column(db.Integer)
    

    # many-to-many association between users and reservations (benefits)
    users = db.relationship('User',
                            secondary=reservations_users,
                            backref=db.backref('reservations', lazy='dynamic'),
                            lazy='dynamic')   
                            
    # many-to-many link between timeslots and reservations
    timeslots = db.relationship('Timeslot',
                            secondary=reservations_timeslots,
                            backref=db.backref('reservations', lazy='dynamic'),
                            lazy='dynamic')
                            
    # reservation owner
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # link to weekdays
    weekday_id = db.Column(db.Integer, db.ForeignKey('weekdays.id'))
    # link to timeslots
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))

    def __repr__(self):
        return '<Reservation %r => %r>' % (self.start_date, self.end_date)




def init_weekdays():
    # initialize table weekdays
    if db.verbosity > 0: print('Initializing table weekdays ...')
    weekdays = [d.strip() for d in '''
        Lundi
        Mardi
        Mercredi
        Jeudi
        Vendredi
        Samedi
        Dimanche'''.split() if d is not '']
        
    for d in weekdays:
        day = Weekday()
        day.name = d
        db.session.add(day)
    
    db.session.commit()
    
    if db.verbosity > 1: 
        for weekday in Weekday.query.all():
            print(weekday)
    if db.verbosity > 0: print('done')
        
    