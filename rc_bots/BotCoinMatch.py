import time

import pyautogui

from rc_util.game_util import *
from rc_util.image_util import *
import random

from PIL import Image

from rc_model.CoinRecognitionModel import CoinModel


class BotCoinMatch:
    def __init__(self):
        self.start_img_path = "rc_items/games/coin_match.png"
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "coin_match"
        self.coin_items = {
            "binance": [],
            "btc": [],
            "eth": [],
            "litecoin": [],
            "monero": [],
            "eos": [],
            "rlt": [],
            "xrp": [],
            "xml": [],
            "tether": [],
        }

    def get_name(self):
        return self.name

    def can_start(self):
        print("coin match can play...")
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return err
        print_log_msg(self.name)
        time.sleep(1)
        print_log("coin_match --> run")
        self.run_game2()
        print_log("coin_match --> finished")
        end_game(self.game_main_path)
        print_log("coin_match --> end")

    def run_game2(self):
        x1 = 476
        x2 = 1023
        y1 = 160
        y2 = 705
        coin_width = 59
        interval = 10
        screen_shot_path = screen_grab()
        for y in range(y1, y2 - coin_width, coin_width+interval):
            for x in range(x1, x2-coin_width, coin_width+interval):
                img_obj = Image.open(screen_shot_path)
                coin_img = cropImgByRect(img_obj, (x, y, x + coin_width,  y + coin_width))
                coin_label = CoinModel.getInstance().predictSingleImg(coin_img)
                self.coin_items[coin_label].append((x+coin_width/2, y+coin_width/2))
        return

    def run_game(self):
        begin_x = 509
        begin_y = 672
        diff_x = 68
        diff_y = 68
        end_x = 987
        end_y = 390
        current_x = 509
        current_y = 672
        while True:
            if current_x > end_x:
                current_x = begin_x
                current_y = current_y - diff_y
            if current_y < end_y:
                current_y = begin_y
            exchange_position_x = current_x + diff_x
            exchange_position_y = current_y - diff_y
            if end_y < exchange_position_y < begin_y:
                pyautogui.click(current_x, exchange_position_y)
                time.sleep(0.1)
                pyautogui.click(current_x, current_y)
                time.sleep(0.5)
                print(f'({current_x}, {exchange_position_y}) <--> ({current_x}, {current_y})')
            if begin_x < exchange_position_x < end_x:
                pyautogui.click(exchange_position_x, current_y)
                time.sleep(0.1)
                pyautogui.click(current_x, current_y)
                time.sleep(0.5)
                print(f'({exchange_position_x}, {current_y}) <--> ({current_x}, {current_y})')
            current_x = current_x + diff_x
            if not in_game(SCORE_IMG_PATH):
                break
