import time

import pyautogui

from rc_util.game_util import *
from rc_util.image_util import *
import random
import time


class BotFlappyRocket:
    def __init__(self):
        self.start_img_path = "rc_items/games/flappy_rocket.png"
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "flappy_rocket"

    def get_name(self):
        return self.name

    def can_start(self):
        print("flappy_rocket can play...")
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path, need_sleep=False)
        if err:
            return err
        print_log_msg(self.name)
        print_log("flappy_rocket --> run")
        self.run_game()
        print_log("flappy_rocket --> finished")
        end_game(self.game_main_path)
        print_log("flappy_rocket --> end")

    def run_game(self):
        start_time = int(time.time())
        start = "not start"
        while True:
            pyautogui.click(469, 670)
            time.sleep(0.17)
            if not in_game(RED_HEART_IMG_PATH):
                if start == "running":
                    break
            else:
                start = "running"
            if time.time() - start_time > 65:
                break
