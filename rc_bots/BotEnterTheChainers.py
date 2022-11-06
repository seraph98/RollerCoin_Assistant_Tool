import time

import pyautogui

from rc_util.game_util import *
from rc_util.image_util import *
import random

#  !!! the page is too slow, so if you play this game, you must get time-out
class BotEnterTheChainers:
    def __init__(self):
        self.start_img_path = "rc_items/games/enter_the_chainers.png"
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "enter_the_chainers"
        self.candidate_position = [
            (801, 308),
            (901, 431),
            (893, 656),
            (570, 612),
            (575, 497),
            (565, 535)
        ]

    def get_name(self):
        return self.name
    def can_start(self):
        print("enter_the_chainers can play..., ", self.start_img_path)
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return not err
        print_log_msg(self.name)
        print_log("enter_the_chainers --> run")
        self.run_game()
        print_log("enter_the_chainers --> finished")
        end_game(self.game_main_path)
        print_log("enter_the_chainers --> end")

    # def run_game(self):
    #     x1 = 400
    #     x2 = 1000
    #     y1 = 150
    #     y2 = 750
    #     while True:
    #         print('-------------')
    #         pic = pyautogui.screenshot(region=(x1, y1, x2, y2,))
    #         width, height = pic.size
    #         for y in range(0, height, 5):
    #             s = ''
    #             for x in range(0, width, 5):
    #                 r, g, b = pic.getpixel((x, y))
    #                 # print(x, y, '-->', r, g, b)
    #                 # s = s + '('+str(r)+','+str(g)+','+str(b)+")"
    #                 if r == 82 and g == 206 and b == 247:
    #                     print('get the enemy: ', x+x1, y+y1)
    #                     mouse_click(x+x1, y+y1, 0.2)
    #             print(s)
    #         if not in_game(RED_HEART_IMG_PATH_2):
    #             break
    #         time.sleep(1)
    def run_game(self):
        x1 = 667
        x2 = 820
        y1 = 450
        y2 = 710
        while True:
            for x in range(x1, x2, 10):
                yy = []
                if abs(x - x1) < 10 or abs(x - x2) < 10:
                    # the outside, needs to be iterate
                    yy = range(y1, y2, 10)
                else:
                    yy = (y1, y1)
                for y in yy:
                    mouse_click(x, y, 0.2)
            if not in_game(RED_HEART_IMG_PATH_2):
                break
            time.sleep(1)
