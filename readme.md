# NYJC Timetable Converter

## Introduction
This is a simple Python script used to automatically add events to calendar applications (Google Calendar, Outlook, etc) according to the user's personal academic timetable provided at NYXchange website.

Python extension ics, which is available at https://pypi.org/project/ics/, is required.

## Quick start
1. Log into the NYXchange website and open up the 10-Day Time Table
2. At the timetable webpage, press F12 to access the developer tools.
3. Refresh the webpage. Under the network tab of the developer tools, you will see files being detected. Right click the file named 'index_ex.php' and save it to the same directory as the converter.py script.
4. Run the converter.py script. An ics file will be generated at the same directory.
5. Import the events to your preferred calendar application using the ics file.
