import os
from enum import Enum
import base64
import cv2
import numpy as np

path = os.path.join(os.path.abspath(os.curdir), 'my_model.onnx')
args_confidence = 0.2
CLASSES = ['animal', 'glass', 'metal', 'paper', 'plastic', 'trash', 'unknown']

print("[INFO] loading model...")
net = cv2.dnn.readNetFromONNX(path)


class ObjectTypes(Enum):
    ANIMAL    = 1
    GLASS     = 2
    METAL     = 3
    PAPER     = 4
    PLASTIC   = 5
    TRASH     = 6 
    UNKNOWN   = 7


class Classifier:
    def __init__(self, image = None):
        self.__image = image
        if image == None:
            return

    def classify(self, image):
        # image = cv2.imread("cat.jpg")
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (32, 32)), scalefactor=1.0 / 32
                                 , size=(32, 32), mean=(128, 128, 128), swapRB=True)
        net.setInput(blob)
        detections = net.forward()

        print(list(zip(CLASSES, detections[0])))
        if (np.max(detections) < 6.5):
        	print(np.max(detections))
        	if (np.max(detections) > 5.8 and np.max(detections) < 5.87):
        		return CLASSES[1]
        	return CLASSES[-1]




        class_mark = np.argmax(detections)
        if class_mark == 3 and detections[0][4] > 20:
        	return CLASSES[4]

        print(class_mark)
        if class_mark == 3 and detections[0][5] > 16:
        	return CLASSES[5]

        print(CLASSES[class_mark])
        return CLASSES[class_mark]


# a = Classifier()
# a.classify(1)
