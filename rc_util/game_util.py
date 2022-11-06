__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:32'

import datetime
import time
import argparse
import cv2
import keyboard
import pyautogui
from MTM import matchTemplates

import rc_util.global_var as gl
from rc_util.image_util import screen_grab
from rc_mail.mail import sendMail
from rc_util.string_util import wrapper_img_path

pyautogui.FAILSAFE = False

COLLECT_PC_IMG_PATH = wrapper_img_path("rc_items/utils/collect_pc.png")
GAIN_POWER_IMG_PATH = wrapper_img_path("rc_items/utils/gain_power.png")
GAIN_POWER_IMG_PATH_2 = wrapper_img_path("rc_items/utils/gain_power_2.png")
GAIN_POWER_IMG_PATH_3 = wrapper_img_path("rc_items/utils/gain_power_3.png")
GAIN_POWER_IMG_PATH_4 = wrapper_img_path("rc_items/utils/gain_power_4.png")
START_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/start_game.png")
START_GAME_IMG_PATH_2 = wrapper_img_path("rc_items/utils/start_game_2.png")
RESTART_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/restart.png")
CHOOSE_GAME_IMG_PATH = wrapper_img_path("rc_items/utils/choose_game.png")
GET_NEW_PC_PATH = wrapper_img_path("rc_items/utils/get_new_pc.png")

RADAR_IMG_PATH = wrapper_img_path("rc_items/utils/radar.png")
GAME_OVER_IMG_PATH = wrapper_img_path("rc_items/utils/game_over.png")
GAME_OVER_IMG_PATH_2 = wrapper_img_path("rc_items/utils/game_over_2.png")
LOSE_CONNECTION_IMG_PATH = "rc_items/utils/lose_conn.png"
GAME_SECTION_IMG_PATH = "rc_items/utils/goto_games.png"
STRICT_VALIDATION_IMG_PATH = "rc_items/utils/strict_validation.png"

RED_HEART_IMG_PATH = "rc_items/utils/red_heart.png"

RED_HEART_IMG_PATH_2 = "rc_items/utils/red_heart_2.png"

parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--validation', '-v', help='human, for strict validation')
args = parser.parse_args()


def mouse_move_left(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x - length, y, 0.2, button='left')


def mouse_move_right(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x + length, y, 0.2, button='left')


def mouse_move_up(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x, y + length, 0.2, button='left')


def mouse_move_down(x, y, length):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x, y - length, 0.2, button='left')


def mouse_click(x, y, wait=0.05):
    pyautogui.click(x, y)
    time.sleep(wait)


def in_game(path=RED_HEART_IMG_PATH):
    return check_image(path)


def find_image(image_path, root_image_path, search_box=None, below_y=0):
    matches = matchTemplates(
        [("img", cv2.imread(image_path))],
        cv2.imread(root_image_path),
        N_object=10,
        score_threshold=0.9,
        searchBox=search_box)
    if len(matches["BBox"]) == 0:
        return None, None
    else:
        for box in matches["BBox"]:
            if below_y == 0 or box[1] < below_y:
                return box[0], box[1]
    return None, None


def check_image(img, below_y=0):
    b, _ = find_image(img, screen_grab(), below_y=0)
    return True if b is not None else False


def click_image(img, wait=0.05,below_y=0):
    time.sleep(wait)
    x, y = find_image(img, screen_grab(), below_y=below_y)
    if x is None or y is None:
        return

    im = cv2.imread(img)
    t_cols, t_rows, _ = im.shape
    mouse_click(x + t_rows * (3 / 5), y + t_cols * (2 / 3))


def start_game(game_block_img_path, below_y=0):
    print('begin start.........')
    click_image(game_block_img_path, below_y=below_y)
    print('end start.........')
    flag = False
    t = 0
    use_version = 1
    while not flag:
        t += 1
        if check_image(RADAR_IMG_PATH):
            print("clicked geetest radar button.")
            click_image(RADAR_IMG_PATH, wait=0.3)
        flag = check_image(START_GAME_IMG_PATH)
        if not flag:
            flag = check_image(START_GAME_IMG_PATH_2)
            if flag:
                use_version = 2
        print(START_GAME_IMG_PATH)
        print(f'flag={flag}')
        time.sleep(0.2)
        print(f't = {t}')
        print('......', not args.validation)

        if check_image(STRICT_VALIDATION_IMG_PATH) and not args.validation:
            click_image(GAME_SECTION_IMG_PATH)
            # maybe blocked by strict validation, should send email and panic
            sendMail("rollercoin", "need validation")
            exit(0)
        if t > 30:
            sendMail("rollercoin", "retry")
            pyautogui.press('f5')
            return "break"
    sx = 0
    sy = 0
    if use_version == 1:
        sx, sy = find_image(START_GAME_IMG_PATH, screen_grab())
    elif use_version == 2:
        sx, sy = find_image(START_GAME_IMG_PATH_2, screen_grab())
    mouse_click(sx + 2, sy + 2, wait=0.05)
    print("begin to count down ...")
    time.sleep(3)
    pyautogui.scroll(40)
    pyautogui.scroll(-2)


def print_log_msg(name):
    game_num = gl.get_value("GAME_NUM")
    print("Starting Game #{!s}: '{}'@{!s}".format(game_num, name,
                                                  datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S %p')))
    gl.set_value('GAME_NUM', game_num + 1)


def print_log(msg):
    print("'{}'@{!s}".format(msg, datetime.datetime.now().strftime('%y-%m-%d %I:%M:%S %p')))


def end_game(game_block_img_path, i=0):
    pyautogui.scroll(10)
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

    if check_image(GAME_OVER_IMG_PATH) or check_image(GAME_OVER_IMG_PATH_2):
        print("gameover")
        if check_image(GAME_SECTION_IMG_PATH):
            click_image(GAME_SECTION_IMG_PATH)
        else:
            pyautogui.press('f5')
        return

    if check_image(START_GAME_IMG_PATH):
        print("start_game")
        click_image(START_GAME_IMG_PATH)

    if check_image(GET_NEW_PC_PATH):
        print("get_new_pc")
        click_image(GET_NEW_PC_PATH)

    keyboard.press_and_release("page up")

    if check_image(LOSE_CONNECTION_IMG_PATH):
        print("lose connection, sending refresh...")
        if check_image(GAME_SECTION_IMG_PATH):
            click_image(GAME_SECTION_IMG_PATH)
        else:
            pyautogui.press('f5')
        return

    if check_image(CHOOSE_GAME_IMG_PATH):
        print("clicked choose game button.")
        click_image(CHOOSE_GAME_IMG_PATH)

    if check_image(COLLECT_PC_IMG_PATH):
        print("clicked collect pc button.")
        click_image(COLLECT_PC_IMG_PATH)

    while not check_image(game_block_img_path):
        print("still waiting...", i)
        time.sleep(1)
        if i > 20:
            print("connection for 20 sec, go to games main")
            click_image(GAME_SECTION_IMG_PATH)
            pyautogui.press('f5')
            return
        return end_game(game_block_img_path, i + 1)
