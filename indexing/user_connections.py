"""
Tutorial: User connection log analysis (using the 'last' command)

Parses the system command 'last' to extract user connection information.
Builds a nested dictionary structure:
    {login: {date: [durations_in_minutes, ...]}}

Usage:
    python user_connections.py
"""

import subprocess
import re

# Run the "last" command and get its output as text
result = subprocess.run(["last"], capture_output=True, text=True)
output = result.stdout

data = {}

# Loop over each line of the result
for line in output.splitlines():
    # Example line: thomas tty2 tty2 Mon Sep 8 08:47 - down (09:18)
    regex = r"^(\w+).*\s(\w{3})\s(\d{1,2}).*\((\d{2}):(\d{2})\)"
    match = re.search(regex, line)

    if match:
        login = match[1]
        month = match[2]
        day = match[3]
        date = f"{month} {day}"
        hours = int(match[4])
        minutes = int(match[5])
        duration = hours * 60 + minutes

        if login not in data:
            data[login] = {}
        if date not in data[login]:
            data[login][date] = []
        data[login][date].append(duration)

# Example of data structure:
# data = {
#     "login1": {"Sep 8": [12, 18], "Sep 7": [45]},
#     "login2": {"Sep 8": [30]}
# }

for login, dates in data.items():
    print(f"{login} connected on:")
    for date, durations in dates.items():
        count = len(durations)
        print(f"  - {date} ({count} times)")
