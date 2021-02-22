import re

invalid_logins = []

with open("auth.log.1", 'r') as file:
    for line in file:
        match = re.search(r'Invalid\suser\s\w+\sfrom\s\d+\.\d+.\d+\.\d+\sport\s\d+', line)
        if match:
            invalid_logins.append(match)

for line in invalid_logins:
    splitline = line.string.split(" ")
    user = splitline[7]
    ip = splitline[9]
    port = splitline[11]
