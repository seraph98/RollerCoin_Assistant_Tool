__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/18 16:15'

import threading

import pyautogui

GAME_LEFT_PADDING = "GAME_LEFT_PADDING"
RECAPTCHA_OFFSET = "RECAPTCHA_OFFSET"
HEAR_IMG_SUFFIX = "HEAR_IMG_SUFFIX"

SCREEN_SETTING = {

    "2560*1440": {
        "LABEL": "2560*1440",
        "GAME_LEFT_PADDING": 20,
        "RECAPTCHA_OFFSET": 22,
        "HEAR_IMG_SUFFIX": ""
    },
    "1920*1080": {
        "LABEL": "1920*1080",
        "GAME_LEFT_PADDING": 20,
        "RECAPTCHA_OFFSET": 27,
        "HEAR_IMG_SUFFIX": "_big"
    }
}


class TargetScreen(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.screen_setting = {}
        width, height = pyautogui.size()
        self._gen_screen_setting(str(width) + "*" + str(height))
        self._height = height
        self._width = width

    def _gen_screen_setting(self, label):
        self.label = label
        settings = SCREEN_SETTING[label]
        self.screen_setting[GAME_LEFT_PADDING] = settings["GAME_LEFT_PADDING"]
        self.screen_setting[RECAPTCHA_OFFSET] = settings["RECAPTCHA_OFFSET"]
        self.screen_setting[HEAR_IMG_SUFFIX] = settings["HEAR_IMG_SUFFIX"]

    def get_center_coordinate(self):
        return tuple(int(self._width / 2), int(self._height / 2))

    def get_recaptcha_center_coordinate(self):
        return tuple(int(self._width / 2), int(self._height / 2) + self.screen_setting[RECAPTCHA_OFFSET])

    def __getitem__(self, item):
        return self.screen_setting[item]

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(TargetScreen, "_instance"):
            with TargetScreen._instance_lock:  # 为了保证线程安全在内部加锁
                if not hasattr(TargetScreen, "_instance"):
                    TargetScreen._instance = TargetScreen(*args, **kwargs)
        return TargetScreen._instance
