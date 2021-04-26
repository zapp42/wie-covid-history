import re
import subprocess
from enum import Enum
from datetime import datetime
import locale
import csv
import sys

command = ['git', 'log', '-p', '--reverse', 'data.html']
p = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
output = p.stdout.read()

State = Enum('State', 'INZIDENZ DATE')

state = State.DATE
current_date = ""
date_inz = {}
locale.setlocale(locale.LC_TIME, "de_DE")
for line in output.split("\n"):
    if re.match(r'^\+.*Fallzahlen', line):
        date_match = re.match(r'^.*Stand: [^,]*, ([^,]*).*', line)
        date = date_match[1]
        current_date = datetime.strptime(date, "%d. %B %Y")
        state = State.DATE
        continue

    if re.match(r'^\+.*Inzidenz von', line):
        if state != State.DATE:
            continue
        inz_match = re.match(r'^.*7-Tage-Inzidenz von ([0-9,]*).*', line)
        inzidenz = inz_match[1]
        date_inz[current_date.strftime("%Y-%m-%d")] = inzidenz.replace(",", ".")
        state = State.INZIDENZ
        continue


csv_writer = csv.writer(sys.stdout, delimiter=',')
for date in date_inz.keys():
    csv_writer.writerow([date, date_inz[date]])
