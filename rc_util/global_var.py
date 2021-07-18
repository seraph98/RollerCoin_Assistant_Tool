__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 11:01'

import datetime


def init():
    global _global_dict
    _global_dict = {}
    _global_dict['GAME_NUM'] = 1
    _global_dict['START_TIME'] = datetime.datetime.now()


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
