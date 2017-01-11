from . import db

from flask.ext.login import UserMixin

db.verbosity = 2


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    sigle = db.Column(db.String(4), unique=True, index=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # link to roles
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # link to reservations (owner)
    owned_reservations = db.relationship('Reservation', backref='owner')
    # link to reservations (teacher) ==> already done through reser
    
    def __repr__(self):
        return '<User %r>' % self.username
        
    @staticmethod
    def insert_admin():
        admin = User()
        admin.username = 'admin'
        admin.email = 'morisodi@edufr.ch'
        admin.first_name = 'Admin'
        admin.last_name = 'Admin'
    
    @staticmethod
    def insert_teachers(sigles):
        for s in sigles:
            teacher = User.query.filter_by(sigle=s).first()
            teacher_role = Role.query.filter_by(name='teacher').one()
            if teacher is None:
                teacher = User(
                    name=sigles[s],
                    sigle=s,
                    email=None,
                    username=s.lower(),
                    password_hash='unsecure',
                    role=teacher_role
                )
                db.session.add(teacher)
                
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    level = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
        
    @staticmethod
    def insert_roles():
        levels = {
            'student' : 1,
            'teacher' : 3,
            'admin' : 100
        }
        
        for r in levels:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r, level=levels[r])
            db.session.add(role)
        db.session.commit()
        

# class StudentGroup(db.Model):
#     __tablename__ = 'student_groups'
# 
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     school_level = db.Column(db.Integer)
# 
#     def __repr__(self):
#         return '<StudentGroup %r>' % self.name
        
        
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    
    # link to reservations
    reservations = db.relationship('Reservation', backref='room')


    def __repr__(self):
        return '<Room %r>' % self.name
        
    @staticmethod
    def insert_rooms(rooms):
        for r in rooms:
            room = Room.query.filter_by(name=r).first()
            if room is None:
                room = Room(name=r)
                db.session.add(room)

        db.session.commit()


class Timeslot(db.Model):
    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True)
    # Représente le numéro de la page horaire dans un jour donné (nombre entier entre 1 et 10 par exemple)
    no = db.Column(db.String(10), unique=True, index=True)
    # Les heures sont de la forme 8h15 ou 10h15 ==> String(5)
    start_time = db.Column(db.String(5))
    end_time = db.Column(db.String(5))
    order = db.Column(db.Integer, unique=True)
    
    # link to reservations ==> already done through reservations_timeslots
    

    def __repr__(self):
        # TODO : il faut encore rajouter le jour auquel cette plage est liée
        return '<Timeslot no=%r>' % self.no

    @staticmethod
    def insert_timeslots(timeslots):
        for order, ts in enumerate(timeslots):
            timeslot = Timeslot(no=ts['no'], start_time=ts['start'], end_time=ts['end'], order=order)
            db.session.add(timeslot)
            
        db.session.commit()

class Weekday(db.Model):
    __tablename__ = 'weekdays'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))
    
    # link to reservations
    reservations = db.relationship('Reservation', backref='weekday')
    

    def __repr__(self):
        # TODO : il faut encore rajouter le jour auquel cette plage est liée
        return '<Weekday id=%r, name=%r>' % (self.id, self.name)
        
        
    @staticmethod
    def insert_days():
        # initialize table weekdays
        string_days = '''
            Lundi
            Mardi
            Mercredi
            Jeudi
            Vendredi
            Samedi
            Dimanche'''
        weekdays = [d.strip() for d in string_days.split() if d is not '']
            
        for d in weekdays:
            day = Weekday()
            day.name = d
            db.session.add(day)
        
        db.session.commit()
        
        

    

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
    # pour les cours de l'horaire officiel, correspond au champ mat_code
    reason_short = db.Column(db.Unicode)
    # pour les cours de l'horaire officiel, correspond au champ mat_libelle
    reason_details = db.Column(db.Unicode)
    # durée de la réservation
    duration = db.Column(db.Integer)
    # nom du groupe classe pour lequel cette réservation a été effectuée, correspond au champ ``CLASSE``
    student_group = db.Column(db.String(20))
    

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
    
    # link to rooms
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))


    def __repr__(self):
        return '<Reservation %r => %r>' % (self.start_date, self.end_date)
