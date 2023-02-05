import json
import requests

url = "https://portal.kuzstu.ru/api/institutes"
site = requests.get(url).text
site = json.loads(site)

institutes = []
for i in site:
    a = []
    a.append(i["id"])
    a.append(i["name"])
    a.append(i["abbr"])
    institutes.append(a)

url = "https://portal.kuzstu.ru/api/directions?institute=5625"
site = requests.get(url).text
site = json.loads(site)
#print(site)
directions_ids = []
for i in site:
    a = []
    a.append(i["id"])
    a.append(i["specialization_name"])
    directions_ids.append(a)
#print(site)

url = "https://portal.kuzstu.ru/api/groups?direction=5625"
site = requests.get(url).text
site = json.loads(site)

groups_names = []
for i in site:
    a = []
    a.append(i["name"])
    groups_names.append(a)

url = "https://portal.kuzstu.ru/api/departments?institute=5625"
site = requests.get(url).text
site = json.loads(site)
print(site)
#print(site)
#print(institutes)
#print(directions_ids)
#print(groups_names)
# print(llll)