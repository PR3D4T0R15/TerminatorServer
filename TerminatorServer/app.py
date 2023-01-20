from flask import Flask
from flask_restful import Api, Resource
import pymongo
import hashlib

app = Flask(__name__) #create app flask
api = Api(app) #create restfulapi

class login(Resource):

    def get(self, name, test):
        return {"name":name, "test":test}

    def post(self):
        return {"data":"Posted"}

api.add_resource(login, "/login/<string:name>/<int:test>")

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

if __name__ == "__main__":
    app.run(debug=True)



