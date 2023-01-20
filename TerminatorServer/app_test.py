import requests

BASE = "http://127.0.0.1:8080"
headers = { "Content-Type" : "application/json", "PASS":"mateusz", "LOGIN":"Mateusz"}

response = requests.get(BASE + "/login", headers=headers)

print(response.json())
