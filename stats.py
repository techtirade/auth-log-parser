import re
import requests
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep

invalid_logins = []
users = []
user_dict = {}
ip_list = []
ip_dict = {}
countries = []
country_dict = {}

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
    ip_list.append(match.group(0))

# ip location check
# via https://ip-api.com/docs/api:batch

# TODO: INFO: Root doesn't appear in this list, why?
clean_ip_list = list(dict.fromkeys(ip_list))
clean_ip_list_chunks = [clean_ip_list[i:i + 99] for i in range(0, len(clean_ip_list), 99)]
data = []
print("IP Lookups ongoing")
for chunk in clean_ip_list_chunks:
    for ip in chunk:
        data.append({"query": "{}".format(ip)})

    req = requests.post('http://ip-api.com/batch', json=data)
    if req.ok:
        for ipinfos in req.json():
            countries.append(ipinfos.get('country'))
    data.clear()

for country in countries:
    country_dict[country] = countries.count(country)

for user in users:
    user_dict[user] = users.count(user)


# Plot origin countries
origin = []
origin_occurences = []

for k, v in country_dict.items():
    if v > 22:
        origin.append(k)
        origin_occurences.append(v)

print("Creating plot for ip origins")
df = pd.DataFrame({"origin":origin,"origin_occurences":origin_occurences})
df_sorted = df.sort_values('origin_occurences',ascending=False)

fig = plt.figure()
plt.bar('origin', 'origin_occurences',data=df_sorted)
plt.xlabel('origin')
plt.ylabel('occurences')
plt.xticks(rotation = 45)
plt.title('Common origins of the bot probes')
plt.gcf().subplots_adjust(bottom=0.20)
plt.savefig("./img/origin.png")

# plot users that are used more than 20 times
cleanuser = []
occurences = []
for k, v in user_dict.items():
    if v > 20:
        cleanuser.append(k)
        occurences.append(v)

print("Creating plot for login users")
df = pd.DataFrame({"usernames":cleanuser,"occurences":occurences})
df_sorted = df.sort_values('occurences',ascending=False)

fig = plt.figure()
plt.bar('usernames', 'occurences',data=df_sorted)
plt.xlabel('usernames')
plt.ylabel('occurences')
plt.title('common usernames used in ssh probes')
plt.savefig("./img/usernames.png")
