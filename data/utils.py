import re
import csv


def extract_timeslots(timeslots_csv='data/timeslots.csv'):
    
    timeslots = []
    
    with open(timeslots_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            timeslots += [dict(row)]

    return timeslots

