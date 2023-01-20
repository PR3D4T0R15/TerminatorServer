from flask import Flask
from flask_restful import Api, Resource
import pymongo

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
