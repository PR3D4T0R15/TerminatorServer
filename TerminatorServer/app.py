from flask import Flask
from flask_restful import Api, Resource
import pymongo

app = Flask(__name__) #create app flask
api = Api(app) #create restfulapi

class Terminator(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(Terminator, "/terminator")

if __name__ == "__main__":
    app.run(debug=True)



