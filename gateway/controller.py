from flask import Flask, request, render_template, redirect, flash, Response
from werkzeug.exceptions import NotFound
import logging.config
import base64
import json
import pickle
import requests
import uuid
import cv2

from service.gateway import *
from config.configurations import Config

app = Flask(__name__)
app.config.from_object(Config)
logging.config.dictConfig(Config.LOGGING_CONFIG)
log = logging.getLogger(__name__)


class GatewayServiceAPI:

    def init_background_model(self, cap):
        initial_frames = []

        for i in range(Config.INITIAL_FRAMES_COUNT):
            ret, img = cap.read()
            if not ret:
                raise GatewayServiceException("Произошла внутрисерверная ошибка")
            img_bytes = pickle.dumps(img)
            initial_frames.append(base64.b64encode(img_bytes).decode('ASCII'))

        jstr = json.dumps({"images": initial_frames})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            r = requests.post(Config.DETECTION_INITMODEL_ENDPOINT,
                            data=jstr,
                            headers=headers)
        except requests.exceptions.RequestException:
            raise GatewayServiceException("Сервис недоступен", name="Detection error: инициализация модели фона", status_code=503)

        return r


    def detect_fragments(self, img, detectorUID):
        img_bytes = pickle.dumps(img)
        jstr = json.dumps({"image": base64.b64encode(img_bytes).decode('ASCII'),
                           "uid": uuid.uuid4().hex,
                           "detectorUID" : detectorUID})
        headers = {'Content-type': 'application/json', 'Accept': 'text/'}
        try:
            r = requests.post(Config.DETECTION_DETECT_ENDPOINT,
                            data=jstr,
                            headers=headers)
        except requests.exceptions.RequestException:
            raise GatewayServiceException("Сервис недоступен", name="Detection error: детекция", status_code=503)

        return r


    def classify_fragments(self, image, uid):
        headers = {'Content-type': 'application/json', 'Accept': 'text/'}
        img_bytes = pickle.dumps(image)
        jstr = json.dumps({"image": base64.b64encode(img_bytes).decode('ASCII'), "uid": uid})
        try:
            r = requests.post(Config.CLASSIFICATION_ENDPOINT,
                            data=jstr,
                            headers=headers)
        except requests.exceptions.RequestException:
            raise GatewayServiceException("Сервис недоступен", name="Classification error", status_code=503)

        return r


gateway = GatewayServiceAPI()
video_process = VideoProcessing(app.config)


@app.errorhandler(NotFound)
def page_not_found(e):
    error = str(e.code) + ": Запрашиваемый ресурс не найден"
    log.exception(error)
    flash(str(error))
    return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/video_feed/<string:filename>')
def video_feed(filename):

    return Response(gen(filename), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(filename):
    try:
        cap = video_process.capture(filename)
        class_status_code = 200

        init_resp_handler = InitializationRespHandler(app.config)
        det_resp_handler = DetectionRespHandler(app.config)
        class_resp_handler = ClassificationRespHandler(app.config)

        # Initialization
        init_resp = gateway.init_background_model(cap)
        detectorUID = init_resp_handler.get_detectorUID(init_resp)

        img_ret, img = cap.read()
        while img_ret:
            # Detection
            det_resp = gateway.detect_fragments(img, detectorUID)
            if det_resp.status_code != requests.codes.ok:
                break
            # fragments contain array of dto
            fragments = det_resp_handler.get_fragments(det_resp)

            # Classification
            for i in range(len(fragments)):
                start_point = (fragments[i]['left'], fragments[i]['top'])
                end_point = (fragments[i]['right'], fragments[i]['bottom'])

                coord_img = class_resp_handler.get_coord_img(img, start_point, end_point)
                class_resp = gateway.classify_fragments(coord_img, fragments[0]['uid'])
                class_status_code = class_resp.status_code
                if class_status_code != requests.codes.ok:
                    break
                classname = class_resp_handler.get_classname(class_resp)
                img = video_process.get_border_text(img, start_point, end_point, classname)
            if class_status_code != requests.codes.ok:
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +
                       cv2.imencode('.jpg', cv2.imread(Config.PATH_TO_ERROR_IMG))[1].tobytes() + b'\r\n')
                video_process.remove_file(filename)
                break
            else:
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img)[1].tobytes() + b'\r\n')
                img_ret, img = cap.read()
        video_process.remove_file(filename)

    except GatewayServiceException:
        error = str(GatewayServiceException.status_code) + ": " + GatewayServiceException.message
        video_process.remove_file(filename)
        log.exception(error)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +
               cv2.imencode('.jpg', cv2.imread(Config.PATH_TO_ERROR_IMG))[1].tobytes() + b'\r\n')


@app.route('/api/v1/gateway/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        video_process.save_file(file)

    except GatewayServiceException as gse:
        error = str(gse.status_code) + ": " + gse.message
        log.exception(error)
        flash(error)

        return redirect('/')

    return render_template("video_player_file.html", filename=file.filename)


