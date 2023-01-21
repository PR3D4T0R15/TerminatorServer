from asyncio.windows_events import NULL
from flask import Flask, request, json, jsonify
from flask_restful import Api, Resource
import mariadb
import hashlib
import json

## TWORZENIE FLASK  I MONGO ##
app = Flask(__name__) #create app flask
api = Api(app) #create restfulapi



## KLASY ZAPYTAN HTTP ##
class login(Resource):

    def get(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        if CheckLogin(login, passwd) == False:
            return "error", 401
        else:
            return "OK", 202

    def put(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        if CheckLogin(login, passwd) == True:
            newPass = request.headers.get("newPASS")
            newLogin = request.headers.get("newLOGIN")
            if newPass != "" and newLogin != "":
                if AddNewUser(newLogin, newPass) == True:
                    return True, 201
                else:
                    return False, 401
        return False, 401


class data(Resource):

    def get(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        listName = request.headers.get("LISTNAME")
        if CheckLogin(login, passwd) == False:
            return "error", 401, {'Content-Type': 'application/json'}
        result = GetListFromServer(login, listName)
        if result == "":
            return "EMPTY", 404
        return json.loads(result)

    def post(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        listName = request.headers.get("LISTNAME")
        body = request.json
        body = json.dumps(body, ensure_ascii=False)
        if CheckLogin(login, passwd) == False:
            return "error", 401, {'Content-Type': 'application/json'}
        if UpdateListOnServer(login, listName, body):
            return "OK", 200, {'Content-Type': 'application/json'}
        else:
            return "ERROR", 400, {'Content-Type': 'application/json'}

    def put(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        listName = request.headers.get("LISTNAME")
        body = request.json
        body = json.dumps(body, ensure_ascii=False)
        if CheckLogin(login, passwd) == False:
            return "error", 401, {'Content-Type': 'application/json'}
        if CreateListOnServer(login, listName, body):
            return "OK", 200, {'Content-Type': 'application/json'}
        else:
            return "ERROR", 400, {'Content-Type': 'application/json'}

    def delete(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        listName = request.headers.get("LISTNAME")
        if CheckLogin(login, passwd) == False:
            return "error", 401, {'Content-Type': 'application/json'}
        if DeleteResource(login, listName):
            return "OK", 200, {'Content-Type': 'application/json'}
        else:
            return "ERROR", 400, {'Content-Type': 'application/json'}


class dataMove(Resource):

    def put(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        listName = request.headers.get("LISTNAME")
        destUser = request.headers.get("DESTUSER")
        if CheckLogin(login, passwd) == False:
            return "error", 401, {'Content-Type': 'application/json'}
        if SendListToUser(login, destUser, listName):
            return "OK", 200, {'Content-Type': 'application/json'}
        else:
            return "ERROR", 400, {'Content-Type': 'application/json'}

api.add_resource(login, "/login")
api.add_resource(data, "/data")
api.add_resource(dataMove, "/datamove")



## FUNKCJE ##
def CheckLogin(login, passwd):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()
    data = (login,)
    query = "SELECT user_name, user_passwd FROM users WHERE user_name = %s;"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    result = cursor.fetchone()
    connection.close()

    if result[0] == login and result[1] == passwd:
        return True
    else:
        return False

def CheckIfDataExist(login, listName):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()

    data = (login,listName)
    query = "SELECT 1 FROM user_lists WHERE user_name = %s AND user_name_list_name = %s"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    result = cursor.fetchone()
    if result:
        if result[0] == 1:
            return True
        else:
            False

def AddNewUser(login, passwd):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()

    data = (login,)
    query = "SELECT user_name FROM users WHERE user_name = %s"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    result = cursor.fetchone()
    if result:
        if result[0] == login:
            return False, 401
    
    data = (login, passwd)
    query = "INSERT INTO users(user_name, user_passwd) VALUES (%s, %s);"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False, 401
    connection.close()
    return True

def GetListFromServer(login, listName):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()

    data = (login, listName)
    query = "SELECT list_content FROM user_lists WHERE user_name = %s AND user_name_list_name = %s;"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    result = cursor.fetchone()
    connection.close()

    result = str(result)
    result = result[2:-3]

    return result

def UpdateListOnServer(login, listName, body):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()
    
    data = (body, login, listName)
    query = "UPDATE user_lists SET list_content = %s WHERE user_name = %s AND user_name_list_name = %s;"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    connection.close()
    return True

def CreateListOnServer(login, listName, body):
    if CheckIfDataExist(login, listName):
        return False

    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()
    
    data = (login, listName, body)
    query = "INSERT INTO user_lists(user_name, user_name_list_name, list_content) VALUES (%s, %s, %s);"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    connection.close()
    return True

def DeleteResource(login, listName):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()

    data = (login, listName)
    query = "DELETE FROM user_lists WHERE user_name = %s AND user_name_list_name = %s;"
    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        print(e)
        return False
    connection.close()
    return True

def SendListToUser(login, destUser, listName):
    if CheckIfDataExist(destUser, listName):
        return False

    jsonData = str(GetListFromServer(login, listName))
    if CreateListOnServer(destUser, listName, jsonData):
        return True
    else:
        return False
    


## URUCHAMIANIE FLASK ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)



