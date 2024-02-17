import logging
from .six import text_type
from kodi_six import xbmc, xbmcaddon, xbmcvfs
from kodi_six.utils import py2_decode

ADDON = xbmcaddon.Addon()
ID = ADDON.getAddonInfo("id")
NAME = ADDON.getAddonInfo("name")
PATH = ADDON.getAddonInfo("path")
ICON = ADDON.getAddonInfo("icon")
PROFILE = ADDON.getAddonInfo("profile")
VERSION = ADDON.getAddonInfo("version")
HOME = xbmcvfs.translatePath("special://home/addons/")
TMP = xbmcvfs.translatePath("special://temp")
if not HOME:
    HOME = '..'

class XBMCHandler(logging.StreamHandler):
    xbmc_levels = {
        'DEBUG': 0,
        'INFO': 2,
        'WARNING': 3,
        'ERROR': 4,
        'CRITICAL': 5,
    }

    def emit(self, record):
        xbmc_level = self.xbmc_levels.get(record.levelname)
        xbmc.log(self.format(record), xbmc_level)

loggers = {}

def _get_logger(name):
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(ID)
        log_level = ADDON.getSetting("log_level")
        if log_level == 0:
            logger.setLevel(logging.CRITICAL)
        elif log_level == 1:
            logger.setLevel(logging.ERROR)
        elif log_level == 2:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)

        handler = XBMCHandler()
        handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
        logger.addHandler(handler)
        return logger

log = _get_logger(__name__)

def append_headers(uri, headers):
    return uri + "|" + "|".join(["%s=%s" % h for h in headers.items()])

# Borrowed from xbmcswift2
def get_setting(key, converter=str, choices=None):
    value = ADDON.getSetting(id=key)
    if converter is text_type or converter is str:
        return py2_decode(value)
    elif converter is bool:
        return value == 'true'
    elif converter is int:
        return int(value)
    elif isinstance(choices, (list, tuple)):
        return choices[int(value)]
    else:
        raise TypeError('Acceptable converters are str, unicode, bool and '
                        'int. Acceptable choices are instances of list '
                        ' or tuple.')

def set_setting(key, val):
    return ADDON.setSetting(id=key, value=val)
