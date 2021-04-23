from ics import Event, Calendar, DisplayAlarm
from datetime import datetime, timedelta
import sys

c = Calendar() # Calendar

# Read php file
doc = []
try:
    with open(r'index_ex.php', 'r') as f:
        for line in f.readlines():
            doc.append(line)
except OSError:
    print('index_ex.php file is not found!')
    sys.exit()

type = str(input('Is the starting week A or B?')).upper() # Starting week
assert type == 'A' or type =='B', 'Only A or B should be provided!'

date = input('Key in the date for the first Monday (MM/DD):') # Initial day input
date = date.split('/')
date = datetime(datetime.now().year, int(date[0]), int(date[1]), 7, 30)

rec = input('Key in how many times the 10-day timetable should be repeated:') # Recurrence input
rec = int(rec)

alarm_switch = str(input('Should alarms be included? (Y/N)'))
assert alarm_switch == 'Y' or 'y' or 'N' or 'n', 'Only Y or N should be provided!'

if alarm_switch == 'Y' or 'y':
    alarm_switch = True
else:
    alarm_switch = False
    
def add_lesson(start, type):
    i = -1 # Counter for days
    k = 0 # Counter for (half) hours
    if type == 'A':
        a = 0
        b = B_line
    else:
        a = B_line
        b = len(doc)
    for m in range(a, b):
        if type + '</td>' in doc[m]:
            i += 1
            k = 0
        elif '<td bgcolor' in doc[m]: # Check for blank time slots
            k += 1
            blank_switch = True
        elif '<td colspan' in doc[m]: # Check for lessons
            # Extract lesson names
            name = doc[m+1].replace('\t\t\t<p class="Large">', '')
            name = name.replace('</p>\n', '')

            # Reformat the lesson names for clarity
            if name == 'pe' or name == 'ct':
                name = name.upper()
            elif name.isupper() == True:
                name = name.upper() + ' Lecture'
            elif name.islower() == True:
                name = name.upper() + ' Tutorial'
            else:
                pass
            name = ' '.join(name.split())
            if 'J2 H2 ' in name:
                name = name.replace('J2 H2 ', '')

            # Extract lesson venues
            location = doc[m+2].replace('\t\t\t<p class="Medium">', '')
            location = location.replace('<br></p>\n', '')

            # Add event with recurrence
            for n in range(rec):
                time_i = start + timedelta(days = i + 14*n, hours = k/2 - 8)
                d = timedelta(hours = int(doc[m][45])/2)

                e = Event()
                e.name = name
                e.location = location
                e.begin = time_i
                e.duration = d

                # Add alarm
                if alarm_switch == True:           
                    if blank_switch == True:
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-15))]
                        blank_switch = False
                    else:
                        e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-5))]
                else:
                    pass

                c.events.add(e)
                
            k += int(doc[m][45])
        else:
            pass


switch = False # Switch for week progression

for m in range(len(doc)):
    if 'B</td>' in doc[m] and switch == False: # Check for week progression
            switch = True
            B_line = m-1
    else:
        pass

if type == 'A':
    add_lesson(date, 'A')
    add_lesson(date + timedelta(days=7), 'B')
else:
    add_lesson(date, 'B')
    add_lesson(date + timedelta(days=7), 'A')

# ics file output
with open('my.ics', 'w') as f:
    f.write(str(c))
