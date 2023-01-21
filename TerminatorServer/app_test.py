import requests

BASE = "http://127.0.0.1:8080"
headers = { "Content-Type" : "application/json", "PASS":"mateusz", "LOGIN":"Mateusz", "newPASS":"jakub", "newLOGIN":"Jakub", "LISTNAME":"Do zrobienia"}

response = requests.get(BASE + "/data", headers=headers)

print(response.json())
