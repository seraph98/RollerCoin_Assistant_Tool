__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 19:39'

import os
import time

from PIL import ImageGrab

from rc_util.string_util import genRandomStr


def screen_grab():
    im = ImageGrab.grab()
    img_name = os.getcwd() + "\\imgs\\full_snap__" + str(int(time.time())) + ".png"
    im.save(img_name, "PNG")
    return img_name


def wrapper_pos(pos):
    return (pos[0], pos[1], pos[2] + pos[0], pos[3] + pos[1])


def grab_img_by_rect(position, save_file=False):
    img = ImageGrab.grab(bbox=position)
    # save to file
    if save_file:
        imgName = os.getcwd() + "\\" + genRandomStr() + ".png"
        img.save(imgName, "PNG")
        print("saved a png file whose name is: ", imgName)
    return img


def cropImgByRect(img, position, save_file=False):
    cropped = img.crop(position)
    if save_file:
        imgName = genRandomStr() + ".png"
        cropped.save(imgName)
        print("saved a png file whose name is: ", imgName)
    return cropped
