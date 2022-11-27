import time

import pyautogui

from rc_util.game_util import *
from rc_util.image_util import *
import random

class Bot2048:
    def __init__(self):
        self.start_img_path = "rc_items/games/2048_gameimg.png"
        self.available_moves = ["right", "left", "up", "down"]
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "2048"

    def get_name(self):
        return self.name

    def can_start(self):
        print("2048 can play...")
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return err
        print_log_msg(self.name)
        time.sleep(1)
        print_log("2048 --> run")
        self.run_game()
        print_log("2048 --> finished")
        end_game(self.game_main_path)
        print_log("2048 --> end")

    def run_game(self):
        while True:
            x, y = find_image("rc_items/2048/center.png", screen_grab())
            if x is None:
                print_log("2048, do not found center")
                time.sleep(1)
                x, y = find_image("rc_items/2048/list.png", screen_grab())
                if x is None:
                    print_log("2048, do not found list")
                    break
            # 690, y=479
            x = 690
            y = 479
            print_log("2048 loop....")
            for _ in range(10):
                action = random.choice(self.available_moves)
                if action == "right":
                    pyautogui.press('right')
                    # mouse_move_right(x,y,200)
                if action == "left":
                    pyautogui.press('left')
                    # mouse_move_left(x,y,200)
                if action == "up":
                    pyautogui.press('up')
                    # mouse_move_up(x,y,200)
                if action == "down":
                    pyautogui.press('down')
                    # mouse_move_down(x,y,200)
                # time.sleep(0.03)
