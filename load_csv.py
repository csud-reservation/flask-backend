import csv

from app.models import *

def load_teachers(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        
        return list(reader)
        
        
def load_items():
    
    file = open("items.csv").read().strip().split(";")
    
    print(file)
        
    return file

def print_row(row):
    for code, value in row.items():
        print(code, " ==> ", value)
        
        
def insert_reservation(db, row, start_date, end_date):
    '''
    
    NUMERO  ==>  1
    POND.  ==>  1
    H.DEBUT  ==>  08h10
    EFFECTIF  ==>  0
    MAT_CODE  ==>  GY
    SALLE  ==>  
    MAT_LIBELLE  ==>  Education physique
    MODALITE  ==>  CG
    CO-ENS.  ==>  N
    DUREE  ==>  2h30
    ALTERNANCE  ==>  H
    PROF_PRENOM  ==>  Marco
    PROF_NOM  ==>  Catillaz
    JOUR  ==>  lundi
    FREQUENCE  ==>  H
    CLASSE  ==>  1EC1

    '''

    # charger le professeur lié à la ligne. Splitter sur les virgules. S'il n'y a pas de virgule, on reçoit une liste contenant un seul élément
    teachers_fnames = [t.strip() for t in row['PROF_PRENOM'].split(',')]
    teachers_lnames = [t.strip() for t in row['PROF_NOM'].split(',')]
    
    #print(teachers_fnames, teachers_lnames)
    teachers = []
    
    for fn, ln in zip(teachers_fnames, teachers_lnames):
        
        teacher = User.query.filter_by(first_name=fn, last_name=ln).first()
        if teacher is None and (fn + ln).strip() != '':
            # Discordance entre le fichier CSV et profs-sigles-courriel.txt
            print('Erreur de chargement : ', row)
            
        teachers.append(teacher)
    
    # Si le champ 'teacher' est vide, il s'agit d'une heure générique qu'il ne faut pas insérer dans l'occupation des salles. Elle n'est là que pour la forme dans le fichier edt.csv ==> autre alternative serait de faire un prétraitement sur ce fichier edt.csv
    # Ne pas tenir compte des heures de gymnastique
    if teachers == [None] or row['MAT_CODE'] == 'GY' or row['SALLE'] == '': return

    duration = int(row['DUREE'].split('h')[0])
    
    # certaines lignes dans le fichier csv se déroulent dans plusieurs salles...
    room_names = [r.strip() for r in row['SALLE'].split(',')]
    rooms = [Room.query.filter_by(name=room_name).first() for room_name in room_names]
    
    weekday = Weekday.query.filter_by(
        # il faut rajouter .title() pour faire lundi ==> Lundi
        name=row['JOUR'].title()
    ).first()
    
    # Chercher l'utilisateur admin (pas effiace ==> requête faite à chaque fois)
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter_by(role=admin_role).first()

    # Si on est à une heure inférieure à 10h, les heures sont notées 08h10 dans le fichier edt.csv mais 8h10 dans la base de données ==> il faut donc transformer ce qui est dans le fichier csv pour correspondre au format de la base de données
    hours, minutes = row['H.DEBUT'].split('h')
    hours = hours[1] if hours[0] == '0' else hours

    start_timeslot = Timeslot.query.filter_by(start_time=hours+'h'+minutes).first()
    timeslots = Timeslot.query.filter(
        Timeslot.order.between(
            start_timeslot.order,
            start_timeslot.order + (duration-1)
        )
    ).all()
    
    
    # Pour chaque salle, il faut faire une réservation identique
    for room in rooms:
        if room is None:
            print("Erreur salle : ", room)
            print(row)
        
            
        reservation = Reservation(
            # dates du début et de fin d'année
            start_date=start_date,
            end_date=end_date,
            reason_short=row['MAT_CODE'],
            reason_details=row['MAT_LIBELLE'],
            duration=duration,
            student_group=row['CLASSE'],
            users=teachers,
            room=room,
            timeslots=timeslots,
            weekday=weekday,
            owner=admin_user
        )
        
        db.session.add(reservation)
    db.session.commit()
    

def load_reservations(db, start_date, end_date, filename='data/edt.csv'):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        
        for row in reader:
            try:
                insert_reservation(db, row, start_date, end_date)
            except Exception as e:
                print("Impossible d'insérer la réservation", row, "raison : ", str(e))
                db.session.rollback()


if __name__ == '__main__':
    db = None
    load_csv(db, 'data/edt.csv')