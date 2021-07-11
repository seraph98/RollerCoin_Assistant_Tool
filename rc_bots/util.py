__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:32'


import datetime
import os
import time
import cv2
import keyboard
import pyautogui
import rc_bots.global_var as gl
from PIL import ImageGrab
from MTM import matchTemplates


def mouse_click(x, y, wait=0.05):
    pyautogui.click(x, y)
    time.sleep(wait)


def screen_grab():
    im = ImageGrab.grab()
    img_name = os.getcwd() + "\\imgs\\full_snap__" + str(int(time.time())) + ".png"
    im.save(img_name, "PNG")
    return img_name


def find_image(image_path, root_image_path):
    matches = matchTemplates(
        [("img", cv2.imread(image_path))],
        cv2.imread(root_image_path),
        N_object=10,
        score_threshold=0.9,
        # maxOverlap=0.25,
        searchBox=None)
    if len(matches["BBox"]) == 0:
        return None, None
    else:
        box = matches["BBox"][0]
        return box[0], box[1]


def check_image(img):
    b, _ = find_image(img, screen_grab())
    return True if b is not None else False


def click_image(img):
    time.sleep(0.05)
    x, y = find_image(img, screen_grab())
    if x is None or y is None:
        return

    im = cv2.imread(img)
    t_cols, t_rows, _ = im.shape
    mouse_click(x + t_rows * (3 / 5), y + t_cols * (2 / 3))



def start_game(start_img_path):
    click_image(start_img_path)
    time.sleep(2)
    if not check_image("rc_items/utils/start_game.png"):
        pyautogui.moveTo(100, 100)
        return True
    sx, sy = find_image("rc_items/utils/start_game.png", screen_grab())
    mouse_click(sx + 2, sy + 2, wait=0.05)
    time.sleep(3)
    return False


def start_game_msg(name):
    game_num = gl.get_value("GAME_NUM")
    print("Starting Game #{!s}: '{}'@{!s}".format(game_num, name, datetime.datetime.now().time()))
    gl.set_value('GAME_NUM', game_num + 1)


def end_game():
    if check_image("rc_items/utils/gain_power.png"):
        click_image("rc_items/utils/gain_power.png")

    if check_image("rc_items/utils/gameover.png"):
        click_image("rc_items/utils/restart.png")

    keyboard.press_and_release("page up")
    if check_image("rc_items/utils/recaptha.png"):
        print("recaptha---")
        keyboard.press_and_release("f5")

    if check_image("rc_items/utils/error2.png"):
        keyboard.press_and_release("f5")

    if check_image("rc_items/utils/choose_game.png"):
        click_image("rc_items/utils/choose_game.png")

    if check_image("rc_items/utils/collect_pc.png"):
        click_image("rc_items/utils/collect_pc.png")

    while not check_image("rc_items/games/coinflip_gameimg.png"):
        print("end game---")
        return end_game()
