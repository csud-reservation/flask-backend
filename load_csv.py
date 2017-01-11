import csv

from app.models import *

def print_row(row):
    for code, value in row.items():
        print(code, " ==> ", value)

def load_csv(filename='edt.csv'):
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
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        return reader
            
        
if __name__ == '__main__':
    load_csv()