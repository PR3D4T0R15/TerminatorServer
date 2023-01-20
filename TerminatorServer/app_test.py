import requests

BASE = "http://127.0.0.1:8080"
headers = { "Content-Type" : "application/json", "PASS":"AdmiN", "LOGIN":"Admin", "newPASS":"jakub", "newLOGIN":"Jakub"}

response = requests.put(BASE + "/login", headers=headers)

print(response.json())
