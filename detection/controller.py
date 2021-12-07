import base64
from config.configurations import Configuration 
from flask import Flask
from flask import request
import json
import logging.config
import pickle
from repositories.repositories import *
from service.detection import *


app = Flask(__name__)
app.config.from_object('config.configurations.Configuration')
detectorRepository = DetectorRepository()
logging.config.dictConfig(Configuration.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class FragmentDTO:
    def __init__(self, uid, left = -1, top = -1, right = -1, bottom = -1):
        self.uid = uid
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
class DTOConvertor:
    def fragmentToDTO(self, uid, fragment):
        return FragmentDTO(uid,
                           fragment.getLeft(),
                           fragment.getTop(),
                           fragment.getRight(),
                           fragment.getBottom())

        
@app.route("/api/v1/detection/initmodel", methods=['POST'])
def initDetector():
    if request.json.get("images") == None:
        logger.exception("400: no images in request")
        return "", 400
    imagesData = request.json['images']
    if len(imagesData) == 0:
        logger.exception("400: less than 1 image in request")
        return "", 400
    images = []
    for imageData in imagesData:
        images.append(pickle.loads(base64.b64decode(imageData)))

    detector = Detector(app.config, images)
    
    uid = detectorRepository.addDetector(detector)
    return json.dumps({"detectorUID" : uid })
  

@app.route("/api/v1/detection/detect", methods=['POST'])
def detect():
    if request.json.get("uid") == None:
        logger.exception("400: no uid in request")
        return "", 400
    uid = request.json["uid"]
    
    if request.json.get("image") == None:
        logger.exception("400: no image in request")
        return "", 400
    image = pickle.loads(base64.b64decode(request.json['image']))
    
    if request.json.get("detectorUID") == None:
        logger.exception("400: no detectorUID in request")
        return "", 400
    detectorUID = request.json["detectorUID"]
    
    if detectorRepository.getDetector(detectorUID) == None:
        logger.exception("400: wrong detectorUID in request")
        return "", 400   
    detector = detectorRepository.getDetector(detectorUID)
    

    fragments = detector.detect(image)
    
    convertor = DTOConvertor()
    DTOFragments = []
    for fragment in fragments:
        obj = convertor.fragmentToDTO(uid, fragment)
        DTOFragments.append(obj.__dict__)
    
    resp = json.dumps({"fragments" : DTOFragments})
    return resp
    
