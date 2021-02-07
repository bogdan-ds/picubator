LOG = True

BME280_PORT = 1
BME280_ADDRESS = 0x77
DHT_SENSOR = 'DHT22'
DHT_PIN = 4
HUMIDIFIER = {
    'pin': 7,
    'lower_threshold': 80,
    'upper_threshold': 90,
}
HEATING = {
    'pin': 8,
    'lower_threshold': 20,
    'upper_threshold': 24,
}
FAN = {
    'pin': 9,
    'periodic_interval_hours': 3,
    'duration_min': 4,
}

log_conf = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'NOTSET',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 5000000,
            'backupCount': 10,
            'filename': 'picubator.log',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'NOTSET',
            'propagate': True
        },
    }
}

SHEETS_CREDENTIAL_PATH = 'client_secret.json'
SPREADSHEET_ID = '1_rF4gtMxrIjKjUxc9P5_oq0cTQ6NBOLV6QZWNF24ehY'
