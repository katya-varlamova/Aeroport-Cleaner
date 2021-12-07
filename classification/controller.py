from flask import Flask, request
import json
import pickle
from service.classification import *


app = Flask(__name__)
classifier = Classifier()


@app.route("/api/v1/classification", methods=['POST'])
def classify():
    uid = request.json["uid"]
    image = pickle.loads(base64.b64decode(request.json['image']))

    global classifier
    className = classifier.classify(image)

    resp = json.dumps({"uid" : uid, "className" : str(className)})
    return resp


