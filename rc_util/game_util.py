__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:32'

import datetime
import time

import cv2
import keyboard
import pyautogui
from mtm import matchTemplates

import rc_util.global_var as gl
from rc_util.image_util import screen_grab
from rc_util.string_util import wrapper_img_path

pyautogui.FAILSAFE = False

COLLECT_PC_IMG_PATH = wrapper_img_path("rc_items/utils/collect_pc.png")
GAIN_POWER_IMG_PATH = wrapper_img_path("rc_items/utils/gain_power.png")
GAIN_POWER_IMG_PATH_2 = wrapper_img_path("rc_items/utils/gain_power_2.png")
GAIN_POWER_IMG_PATH_3 = wrapper_img_path("rc_items/utils/gain_power_3.png")
GAIN_POWER_IMG_PATH_4 = wrapper_img_path("rc_items/utils/gain_power_4.png")
START_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/start_game.png")
RESTART_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/restart.png")
CHOOSE_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/choose_game.png")

RADAR_IMG_PATH = wrapper_img_path("rc_items/utils/radar.png")
GAME_OVER_IMG_PATH = wrapper_img_path("rc_items/utils/game_over.png")
LOSE_CONNECTION_IMG_PATH = "rc_items/utils/lose_conn.png"
GAME_SECTION_IMG_PATH = "rc_items/utils/goto_games.png"


def mouse_move_left(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x-length, y, button='left')


def mouse_move_right(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x+length, y, button='left')


def mouse_move_up(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x, y+length, button='left')


def mouse_move_down(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x, y-length, button='left')

def mouse_click(x, y, wait=0.05):
    pyautogui.click(x, y)
    time.sleep(wait)


def find_image(image_path, root_image_path, search_box=None):
    matches = matchTemplates(
        [("img", cv2.imread(image_path))],
        cv2.imread(root_image_path),
        N_object=10,
        score_threshold=0.9,
        searchBox=search_box)
    if len(matches["BBox"]) == 0:
        return None, None
    else:
        box = matches["BBox"][0]
        return box[0], box[1]


def check_image(img):
    b, _ = find_image(img, screen_grab())
    return True if b is not None else False


def click_image(img, wait=0.05):
    time.sleep(wait)
    x, y = find_image(img, screen_grab())
    if x is None or y is None:
        return

    im = cv2.imread(img)
    t_cols, t_rows, _ = im.shape
    mouse_click(x + t_rows * (3 / 5), y + t_cols * (2 / 3))


def start_game(game_block_img_path):
    click_image(game_block_img_path)
    flag = False
    t = 0
    while not flag:
        t += 1
        if check_image(RADAR_IMG_PATH):
            print("clicked geetest radar button.")
            click_image(RADAR_IMG_PATH, wait=0.3)
        flag = check_image(START_GAME_IMG_PATH)
        print(START_GAME_IMG_PATH)
        print(f'flag={flag}')
        time.sleep(0.2)
        print(f't = {t}')
        if t > 6:
            click_image(GAME_SECTION_IMG_PATH)
            return "break"
    sx, sy = find_image(START_GAME_IMG_PATH, screen_grab())
    mouse_click(sx + 2, sy + 2, wait=0.05)
    print("begin to count down ...")
    time.sleep(3)


def print_log_msg(name):
    game_num = gl.get_value("GAME_NUM")
    print("Starting Game #{!s}: '{}'@{!s}".format(game_num, name,
                                                  datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S %p')))
    gl.set_value('GAME_NUM', game_num + 1)


def end_game(game_block_img_path):
    if check_image(GAIN_POWER_IMG_PATH):
        print("clicked gain power button.")
        click_image(GAIN_POWER_IMG_PATH)

    if check_image(GAIN_POWER_IMG_PATH_2):
        print("clicked gain power button_2.")
        click_image(GAIN_POWER_IMG_PATH_2)

    if check_image(GAIN_POWER_IMG_PATH_3):
        print("clicked gain power button_3.")
        click_image(GAIN_POWER_IMG_PATH_3)

    if check_image(GAIN_POWER_IMG_PATH_4):
        print("clicked gain power button_4.")
        click_image(GAIN_POWER_IMG_PATH_4)

    if check_image(GAME_OVER_IMG_PATH):
        print("gameover")
        click_image(GAME_SECTION_IMG_PATH)

    if check_image(START_GAME_IMG_PATH):
        print("start_game")
        click_image(START_GAME_IMG_PATH)

    keyboard.press_and_release("page up")

    if check_image(LOSE_CONNECTION_IMG_PATH):
        print("lose connection, sending refresh...")
        keyboard.press_and_release("f5")

    if check_image(CHOOSE_GAME_IMG_PATH):
        print("clicked choose game button.")
        click_image(CHOOSE_GAME_IMG_PATH)

    if check_image(COLLECT_PC_IMG_PATH):
        print("clicked collect pc button.")
        click_image(COLLECT_PC_IMG_PATH)

    while not check_image(game_block_img_path):
        print("still waiting...")
        return end_game(game_block_img_path)
