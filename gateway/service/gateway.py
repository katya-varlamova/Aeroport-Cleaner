import cv2
import os
import requests


class GatewayServiceException(Exception):
    status_code = 500
    name = "Gateway error"
    message = "Ошибка шлюза"

    def __init__(self, message, name=None, status_code=None):
        super().__init__()
        self.message = message
        if name is not None:
            self.name = name
        if status_code is not None:
            self.status_code = status_code


class VideoProcessing:
    def __init__(self, config):
        self.config = config

    def capture(self, filename):
        cap = cv2.VideoCapture(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config["PATH_TO_VIDEO"] + filename))
        if not cap.isOpened():
            raise GatewayServiceException("Произошла внутрисерверная ошибка")
        return cap

    def save_file(self, file):
        if not file:
            raise GatewayServiceException("Файл не найден", name="Gateway error", status_code=404)
        target = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config["PATH_TO_VIDEO"])
        filename = file.filename
        destination = '/'.join([target, filename])
        try:
            file.save(destination)
        except:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")

    def remove_file(self, filename):
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config["PATH_TO_VIDEO"] + filename)
            os.remove(path)
        except:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")

    def get_border_text(self, image, start_point, end_point, classname):
        try:
            image = cv2.rectangle(image, start_point, end_point, self.config["COLOR_BORDER"],
                                  self.config["THICKNESS_BORDER"])
            image = cv2.putText(img=image,
                                text=classname,
                                org=start_point,
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=self.config["FONT_SCALE"],
                                color=self.config["COLOR_TEXT"],
                                thickness=self.config["THICKNESS_TEXT"])
        except:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")
            return

        return image

    def get_resp_img(self):
        return b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', cv2.imread(self.config["PATH_TO_ERROR_IMG_GATEWAY"]))[1].tobytes() + b'\r\n'


class InitializationRespHandler:
    def __init__(self, config):
        self.config = config

    def get_detectorUID(self, resp):
        if resp.status_code != requests.codes.ok:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")
        return resp.json()['detectorUID']


class DetectionRespHandler:
    def __init__(self, config):
        self.config = config

    def get_fragments(self, resp):
        if resp.status_code != requests.codes.ok:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")
        return resp.json()['fragments']


class ClassificationRespHandler:
    def __init__(self, config):
        self.config = config

    def get_coord_img(self, img, start_point, end_point):
        return img[start_point[1]:end_point[1], start_point[0]:end_point[0]]

    def get_classname(self, resp):
        if resp.status_code != requests.codes.ok:
            raise GatewayServiceException("Произошла внутрисерверная ошибка")
        return resp.json()['className']
