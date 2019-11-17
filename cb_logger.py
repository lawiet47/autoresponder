import logging
from colorlog import ColoredFormatter
LOG_LEVEL = logging.INFO
LOGFORMAT = "%(log_color)s%(levelname)-8s%(reset)s | %(message_log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT,
        datefmt=None,
        reset=True,
        log_colors={
                'SUCCESS':  'thin_black,bg_green',
                'DEBUG':    'thin_black,bg_white',
                'INFO':     'thin_black,bg_cyan',
                'WARNING':  'thin_black,bg_yellow',
                'ERROR':    'thin_black,bg_purple',
                'CRITICAL': 'thin_black,bg_red',
        },
        secondary_log_colors={
        	'message': {
                'SUCCESS':  'thin,green',
	        	'DEBUG':    'bold,white',
	            'INFO':     'thin,cyan',
	            'WARNING':  'thin,yellow',
	            'ERROR':    'thin,purple',
	            'CRITICAL': 'bold,red',
            }
        },
        )

SUCCESS=25
logging.addLevelName(SUCCESS, "SUCCESS")
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
