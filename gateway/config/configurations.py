class Config(object):
    DETECTION_INITMODEL_ENDPOINT = "http://127.0.0.1:5001/api/v1/detection/initmodel"
    DETECTION_DETECT_ENDPOINT = "http://127.0.0.1:5001/api/v1/detection/detect"
    CLASSIFICATION_ENDPOINT = "http://127.0.0.1:5002/api/v1/classification"
    SECRET_KEY = "akscjvhv3asdfhn"
    INITIAL_FRAMES_COUNT = 20
    PATH_TO_VIDEO = "../static/video/"
    PATH_TO_ERROR_IMG = "static/images/error.jpg"

    #red color in RGB
    COLOR_BORDER = (0,0,255)
    # black color in RGB
    COLOR_TEXT = (0,0,0)
    THICKNESS_BORDER = 2
    THICKNESS_TEXT = 2
    FONT_SCALE = 1

    LOGGING_CONFIG = {
        "version": 1,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "config/file.log"
            }
        },
        "loggers": {
            "controller": {
                "handlers": ["fileHandler"],
                "level": "DEBUG",
            }
        },
        "formatters": {
            "myFormatter": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }


