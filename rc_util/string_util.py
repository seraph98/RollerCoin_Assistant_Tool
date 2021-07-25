__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 18:04'

import random
import string

from rc_model.ScreenSetting import TargetScreen, HEAR_IMG_SUFFIX


def genRandomStr(string_length=10):
    letters_and_num = string.hexdigits
    return ''.join(random.choice(letters_and_num) for _ in range(string_length))


def wrapper_img_path(path):
    screen_info = TargetScreen.getInstance()
    suffix = screen_info[HEAR_IMG_SUFFIX]
    result = path
    if suffix is not None and suffix != "":
        part1, part2 = path.split(".")
        result = "".join([part1, suffix, ".", part2])
    print("result ->", result)
    return result
