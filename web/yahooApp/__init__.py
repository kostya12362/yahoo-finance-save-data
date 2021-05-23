from flask import Flask, jsonify
from flask_restful import Api
from .views import HelloWorld, DownloadFile
from pathlib import Path

import sys
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
import config

app = Flask(__name__)
api = Api(app)
app.config.from_object("yahooApp.config")

@app.route("/")
def hello_world():
    print()
    return jsonify(hello=f"http://localhost:5000/pd/")

api.add_resource(HelloWorld, '/<string:symbol>/')
api.add_resource(DownloadFile, '/<string:symbol>/download/')