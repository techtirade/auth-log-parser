import re

invalid_logins = []
users = []
user_dict = {}
ip = []

with open("auth.log.testfile", 'r') as file:
    for line in file:
        match = re.search(r'Invalid\suser\s\w+\sfrom\s\d+\.\d+.\d+\.\d+\sport\s\d+', line)
        if match:
            invalid_logins.append(match)

for line in invalid_logins:
    # USER
    match = re.search("user\s\w+", line.string)
    matchstring = match.group(0)
    user = matchstring.split(" ")[1]
    users.append(user)

    # IP
    match = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line.string)
    ip.append(match.group(0))

# TODO: INFO: Root doesn't appear in this list, why?
# TODO: find way to automate lookup of ip origin
for user in users:
    user_dict[user] = users.count(user)
