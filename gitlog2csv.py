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
old_parser = True
capture = False
locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
for line in output.split("\n"):
    if re.match(r'^commit 5f3c2d45a45fb526a07e1f9b4dc880b638da6dd3', line):
        old_parser = False
        continue

    if old_parser:
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
    else:
        if re.match(r'^ <p><strong>7-Tage-Inzidenz', line):
            capture = True
            continue
        if capture:
            new_inzidenz = re.match(r'^\+<li>(.*) - (.*)</li>', line)
            if new_inzidenz:
                current_date = datetime.strptime(new_inzidenz[1], "%d. %B %Y")
                inzidenz = new_inzidenz[2].replace(",", ".")
                date_inz[current_date.strftime("%Y-%m-%d")] = inzidenz
                capture = False
                continue

csv_writer = csv.writer(sys.stdout, delimiter=',')
for date in date_inz.keys():
    csv_writer.writerow([date, date_inz[date]])
