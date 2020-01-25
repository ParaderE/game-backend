import json
import requests

login = input()
password = input()
acc = login + password

data = {
    "account": acc
}

raw_res = requests.post("http://localhost:5000/register/", json=data).text
print(raw_res)
json_res = json.loads(raw_res)
print(json_res["is_free"])