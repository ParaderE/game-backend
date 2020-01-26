import requests

payload = """{"account": "test test"}"""
res = requests.post("http://localhost:5000/test_json", json=payload)
print(res.text)