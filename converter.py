from ics import Event, Calendar
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

'''type = str(input('Is the starting week A or B?')).upper() # Starting week
assert type == 'A' or type =='B', 'Only A or B should be provided!'''

date = input('Key in the date for Mon A (MM/DD):') # Initial day input
date = date.split('/')
date = datetime(2021, int(date[0]), int(date[1]), 7, 30)

rec = input('Key in how many times the timetable should be repeated:') # Recurrence input
rec = int(rec)

i = -1 # Counter for days
k = 0 # Counter for (half) hours
switch = False # Switch from week to week 

for m in range(len(doc)):
    if 'style="padding:5px; border:1px solid black' in doc[m]:
        i += 1
        k = 0
        if 'B</td>' in doc[m] and switch == False: # Check for week progression
            i += 2
            switch = True
    elif '<td bgcolor' in doc[m]: # Check for blank time slots
        k += 1
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
            time_i = date + timedelta(days = i + 14*n, hours = k/2 - 8)
            d = timedelta(hours = int(doc[m][45])/2)

            e = Event()
            e.name = name
            e.location = location
            e.begin = time_i
            e.duration = d
            c.events.add(e)

        k += int(doc[m][45])
    else:
        pass

# ics file output
with open('my.ics', 'w') as f:
    f.write(str(c))