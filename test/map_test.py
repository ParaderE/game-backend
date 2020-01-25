import json
import requests

login = input()
password = input()
acc = login + password

data = {
    "size": [500, 500],
    'position': [2000, 1200],
    'account': login + " " + password
}

raw_res = requests.post("http://localhost:5000/get_objects/", json=data).text
print(raw_res)