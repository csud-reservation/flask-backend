from . import db
import string
import random
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
db.verbosity = 2

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    sigle = db.Column(db.String(4), unique=True, index=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    # pas besoin de username puisque l'on utilise le courriel pour se logueur
    # username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # link to roles
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # link to reservations (owner)
    owned_reservations = db.relationship('Reservation', backref='owner')
    # link to reservations (teacher) ==> already done through reservation
    
    def __repr__(self):
        return '<User %d, %r>' % (self.id, self.email)

    @staticmethod
    def password_generator(length=8) :
        return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def reset_user_passwd(sigle, passwd):
        user = User.query.filter_by(sigle=sigle).one().set_password(passwd)
        db.session.commit()
        
    @staticmethod
    def insert_admin():
        admin_role = Role.query.filter_by(name='admin').first()
        admin = User.query.filter_by(role=admin_role).first() or User(
            first_name="Administrateur",
            last_name="Système réservation CSUD",
            email="morisodi@edufr.ch",
            password_hash='temp_unsecure',
            sigle='MORI',
            role=admin_role
        )
        
        password = User.password_generator()
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

    @staticmethod
    def remove_all_teachers():
        raise NotImplementedError("To be done")
    
    @staticmethod
    def insert_teachers(teachers):
        
        for csv_teacher in teachers:
            teacher = User.query.filter_by(sigle=csv_teacher['Sigle']).first()
            

            csv_role = csv_teacher['Fonction Identifiant FR']
            try:
                role = Role.query.filter_by(
                    description=csv_role
                ).one()
            except Exception as e:
                role = Role.query.filter_by(name='teacher').one()
                print("enseignant csv", csv_teacher)
                print("Rôle inconnu : ", csv_role, "... J'ai mis 'Enseignant' à la place !")

            
            # or print("Problème pour l'enseignant", csv_teacher, " : le rôle", csv_role, "n'existe pas dans la base de données.")
            
            if teacher is None:
                teacher = User(
                    first_name=csv_teacher['Prénom'],
                    last_name=csv_teacher['Nom'],
                    sigle=csv_teacher['Sigle'],
                    email=csv_teacher['Email Ecole'],
                    password_hash='temp',
                    role=role
                )

                teacher.set_password(User.password_generator())
                db.session.add(teacher)
                
        db.session.commit()
        
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

        if current_app.config['NOTIFY_PASSWD'] == 'CSV_FILE':
            # pas performant lors du chargement initial mais ce n'est pas très
            # grave, ... on pourrait passer en option le fichier csv à écrire
            print("Création du compte ", self.email, " avec mot de passe", password)
            with open('account_password.csv','a') as csv_file:     
                csv_file.write(self.email + ";" + password + "\n")
            
        if current_app.config['NOTIFY_PASSWD'] == 'EMAIL':
            # envoyer le mot de passe par courriel ...
            pass
        
            


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(128))
    level = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
        
    @staticmethod
    def insert_roles():
        roles = {
            # étudiants
            'student' : (1, 'Étudiant'),
            # stagiaires
            'intern' : (2, 'Stag_ens'),
            # enseignants
            'teacher' : (3, 'Enseignant'),
            # remplaçant
            'substitute' : (3, 'Rempl'),
            # personnel administratif
            'mediator' : (3, 'Médiation'),
            # personnel administratif
            'aumonerie' : (3, 'Aumonerie'),
            # personnel administratif
            'staff' : (20, 'Admin'),
            # administrateur
            'admin' : (100, 'Administrateur des réservations'),
        }
        
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(
                    name=r,
                    level=roles[r][0],
                    description=roles[r][1]
                )
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
        
        
class Item(db.Model):
    __tablename__="items"
        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_types.id'))
    
    # link to reservations
    reservations = db.relationship('Reservation', backref='item')
    
    
    
    
    @staticmethod
    def insert_items(items):
        for i in items:
            print(i)
            i_t = Item_Type.query.filter_by(name=i[1]).first()
            item = Item(name=i[0], item_type_id =i_t.id)
            db.session.add(item)

        db.session.commit()
    
    def __repr__(self):
        return '<Item %r>' % self.name
        
class Item_Type(db.Model):
    __tablename__ ="item_types"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(10))
    
    item = db.relationship('Item', backref='item_type')
    
    
    
    @staticmethod
    def insert_item_types():
        item_types = ["Caméra", "Trépied", "Appareil photo", "Visualiseur", "Ordinateur", "Autre"]
        
        for i in item_types:
            item_type = Item_Type(name=i)
            db.session.add(item_type)
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
        return '<Timeslot no=%r, start_time=%r>' % (self.no, self.start_time)

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
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    
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
    reason_short = db.Column(db.String(128))
    # pour les cours de l'horaire officiel, correspond au champ mat_libelle
    reason_details = db.Column(db.String(128))
    # durée de la réservation (en nombres de plages horaires)
    # ATTENTION : cela constitue une redondance si on lie aussi toutes les pages horaires avec les réservations
    duration = db.Column(db.Integer)
    # nom du groupe classe pour lequel cette réservation a été effectuée, correspond au champ ``CLASSE``
    student_group = db.Column(db.String(60))
    

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
    
    
    # link to items
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    



    def __repr__(self):
        return '<Reservation %r => %r>' % (self.start_date, self.end_date)
