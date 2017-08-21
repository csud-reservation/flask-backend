import re
import csv

def extract_sigles(timetable_file="data/timetable.txt"):
    
    sigles = {}
    
    with open(timetable_file, 'r', encoding='utf-8') as fd:
        for line in fd:
            prof_pattern = r'^\s*(?P<name>.*) \((?P<sigle>[A-Z]{4})\)$'
            prog = re.compile(prof_pattern)
            m = prog.match(line)
            if m:
                (name, sigle) = m.groups()
                if sigle not in sigles:
                    sigles[sigle] = name
                    
    return sigles


def extract_rooms(timetable_file="data/rooms.txt"):
    
    rooms = []
    
    with open(timetable_file, 'r', encoding='utf-8') as fd:
        for line in fd:
            prof_pattern = r'^Salle (.*)$'
            prog = re.compile(prof_pattern)
            m = prog.match(line)
            if m:
                name = m.group(1)
                if name not in rooms:
                    rooms += [name]
                    
    return rooms


        
def extract_timeslots(timeslots_csv='data/timeslots.csv'):
    
    timeslots = []
    
    with open(timeslots_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            timeslots += [dict(row)]

    return timeslots

