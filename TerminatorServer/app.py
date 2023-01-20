from flask import Flask, request
from flask_restful import Api, Resource
import mariadb
import hashlib


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
            return {"user":login, "status":"logged"}

    def put(self):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        return {"user":login, "status":"created"}

api.add_resource(login, "/login")

class data(Resource):

    def get(self, name, test):
        passwd = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        return {"name":name, "test":test}

    def put(self):

        return {"data":"Updated"}

    def delete(self):
        return {"data":"Deleted"}

api.add_resource(data, "/data/<string:name>/<int:test>")

class dataMove(Resource):

    def get(self, name, test):
        return {"name":name, "test":test}

    def post(self):
        return {"data":"Posted"}

api.add_resource(dataMove, "/datamove/<string:name>/<int:test>")



## FUNKCJE ##
def CheckLogin(login, passwd):
    connection = mariadb.connect(user="python", password="python1234", host="127.0.0.1", port=3306, database="Terminator")
    cursor = connection.cursor()
    query = "SELECT user_name, user_passwd FROM users WHERE user_name = " + "\"" + login + "\";"
    cursor.execute(query)

    if cursor["user_name"] == login and cursor["user_passwd"] == passwd:
        return True
    else:
        return False

def AddNewUser(login, passwd):
    



## URUCHAMIANIE FLASK ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)



