from ics import Event, Calendar
from datetime import datetime, timedelta
import os

c = Calendar()

date = input('Key in the date for Mon A (MM/DD):')
date = date.split('/')
date = datetime(2021, int(date[0]), int(date[1]), 7, 30)

rec = input('Key in how many times the timetable should be repeated:')
rec = int(rec)

# rename = 

doc = []
with open(r'index_ex.php', 'r') as f:
    for line in f.readlines():
        doc.append(line)

i = -1
k = 0
switch = False

for m in range(len(doc)):
    if 'style="padding:5px; border:1px solid black' in doc[m]:
        i += 1
        k = 0
        if 'B</td>' in doc[m] and switch == False:
            i += 2
            switch = True
    elif '<td bgcolor' in doc[m]:
        k += 1
    elif '<td colspan' in doc[m]:
        name = doc[m+1].replace('\t\t\t<p class="Large">', '')
        name = name.replace('</p>\n', '')
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

        location = doc[m+2].replace('\t\t\t<p class="Medium">', '')
        location = location.replace('<br></p>\n', '')
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

with open('my.ics', 'w') as f:
    f.write(str(c))
