import uuid
class DetectorRepository:
    def __init__(self):
        self.__detectors = {}
    def addDetector(self, detector):
        uid = str(uuid.uuid4())
        self.__detectors[uid] = detector
        return uid
    def deleteDetector(self, uid):
        self.__detectors.pop(uid)
    def getDetector(self, uid):
        return self.__detectors.get(uid)
