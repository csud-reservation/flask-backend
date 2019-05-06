import csv
import codecs

# Pour le fuzzy matching permettant de faire le lien entre les noms et prénoms
# selon le secrétariat et selon EDT ...
from fuzzywuzzy import process

from app.models import *


def load_teachers(filename, encoding='cp1252'):
    #with open(filename, 'rb', encoding='cp1252') as csvfile:
    with codecs.open(filename,"rb",encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        
        return list(reader)
        
        
def load_items():
    
    file = open("data/items.csv").readlines()
    
    item_list = []
    
    for line in file:
        item_list.append(line.strip().split(";"))
                
    return item_list


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
    errors = []

    # Tous les noms et prénom selon la base de données pour faire le matching
    # flou pour permettre de faire le lien entre le fichier des secrétaires et
    # celui de EDT qui ne sont parfois pas synchronisés
    choices = [t.first_name + '|' + t.last_name for t in User.query.all()]
    
    for fn, ln in zip(teachers_fnames, teachers_lnames):
        
        teacher = User.query.filter_by(first_name=fn, last_name=ln).first()
        if teacher is None and (fn + ln).strip() != '':
            # Essayer de trouver la meilleure correspondance ... avec une
            # recherche floue
            match = process.extract(fn + ln, choices, limit=1)
            db_full_name = match[0][0]
            print('Association entre ', fn + ln, "et", match[0][0], match[0][1])
            fn, ln = db_full_name.split('|')
            teacher = User.query.filter_by(first_name=fn, last_name=ln).first()
            
            #  Discordance entre le fichier CSV et
            # profs-sigles-courriel.txt
            print('Erreur de chargement (problème nommage du prof) : ', row)
            errors.append(row)
            
        teachers.append(teacher)

    with open('profs-error.log', 'w') as fd:
        for e in errors:
            fd.write(str(e) + '\n')
    
    # Si le champ 'teacher' est vide, il s'agit d'une heure générique qu'il ne
    # faut pas insérer dans l'occupation des salles. Elle n'est là que pour la
    # forme dans le fichier edt.csv ==> autre alternative serait de faire un
    # prétraitement sur ce fichier edt.csv Ne pas tenir compte des heures de
    # gymnastique
    if teachers == [None] or row['MAT_CODE'] == 'GY' or row['SALLE'] == '': return

    duration = int(row['DUREE'].split('h')[0])
    
    # certaines lignes dans le fichier csv se déroulent dans plusieurs salles...
    room_names = [r.strip() for r in row['SALLE'].split(',')]
    # si la salle n'existe pas encore dans la base de données (retourne None),
    # alors elle est crée
    rooms = [Room.query.filter_by(name=room_name).first() or Room(name=room_name) for room_name in room_names]
    
    weekday = Weekday.query.filter_by(
        # il faut rajouter .title() pour faire lundi ==> Lundi
        name=row['JOUR'].title()
    ).first()
    
    # Chercher l'utilisateur admin (pas effiace ==> requête faite à chaque fois)
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter_by(role=admin_role).first()

    # Si on est à une heure inférieure à 10h, les heures sont notées 08h10 dans
    # le fichier edt.csv mais 8h10 dans la base de données ==> il faut donc
    # transformer ce qui est dans le fichier csv pour correspondre au format de
    # la base de données
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
    

def load_reservations(db, start_date, end_date, filename='data/edt.csv', encoding='cp1252'):
    with codecs.open(filename,"rb", encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        
        for row in reader:
            try:
                insert_reservation(db, row, start_date, end_date)
            except Exception as e:
                print("Impossible d'insérer la réservation", row, "raison : ", str(e))
                print("Erreur", e)
                db.session.rollback()


if __name__ == '__main__':
    db = None
    load_csv(db, 'data/edt.csv')