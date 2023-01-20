from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import hashlib


## TWORZENIE FLASK  I MONGO ##
app = Flask(__name__) #create app flask
api = Api(app) #create restfulapi

## KLASY ZAPYTAN HTTP ##
class login(Resource):

    def get(self):
        haslo = request.headers.get("PASS")
        login = request.headers.get("LOGIN")
        return haslo + login


api.add_resource(login, "/login")

class data(Resource):

    def get(self, name, test):
        return {"name":name, "test":test}

    def post(self):
        return {"data":"Posted"}

api.add_resource(data, "/data/<string:name>/<int:test>")

class dataMove(Resource):

    def get(self, name, test):
        return {"name":name, "test":test}

    def post(self):
        return {"data":"Posted"}

api.add_resource(dataMove, "/datamove/<string:name>/<int:test>")

## FUNKCJE ##



## URUCHAMIANIE FLASK ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)



