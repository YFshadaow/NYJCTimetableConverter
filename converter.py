from ics import Event, Calendar
from datetime import datetime, timedelta
from pytz import UTC
import os

c = Calendar()

date = datetime(2021, 2, 15, 7, 30)
rec = 2

doc = []
with open(r'calendar.php', 'r') as f:
    for line in f.readlines():
        doc.append(line)

doc = doc[35:]
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

        location = doc[m+2].replace('\t\t\t<p class="Medium">', '')
        location = location.replace('<br></p>\n', '')

        time_i = date + timedelta(days = i, hours = k/2 - 8)
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
