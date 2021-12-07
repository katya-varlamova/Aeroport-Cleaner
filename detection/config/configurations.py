class Configuration(object):
     HISTORY = 60
     THRESHOLD = 50
     BACKGROUND_RATIO = 0.8
     NMIXTURES = 10
     CLOSING_RECT = (9, 9)
     OPENING_RECT = (21, 21)
     INDENT = 20
     
     LOGGING_CONFIG = {
        "version": 1,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "config/config.log"
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
