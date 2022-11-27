__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:30'

import random
from time import sleep

from PIL import Image

from rc_model.CoinRecognitionModel import CoinModel
from rc_util.game_util import *
from rc_util.image_util import *
from rc_util.string_util import wrapper_img_path


class BotCoinFlipBot:
    def __init__(self):
        self.head_img_path = wrapper_img_path("rc_items/games/coinflip_game_head_img.png")
        self.card_back_img_path = wrapper_img_path("rc_items/coinflip/coinflip_back.png")
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")

        self.name = "CoinFlip"

        self.coin_pos = []
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
        return check_image(self.head_img_path)

    def play(self):
        err = start_game(self.head_img_path)
        if err:
            return err
        print_log_msg(self.name)
        sleep(2)
        self.get_coin_fields()
        self.check_coins()
        self.match_coins()
        end_game(self.game_main_path)

    def get_coin_fields(self):
        screen = cv2.imread(screen_grab())
        matches = matchTemplates(
            [("img", cv2.imread(self.card_back_img_path))],
            screen,
            N_object=float("inf"),
            score_threshold=0.5,
            searchBox=None)
        for i in range(len(matches['BBox'])):
            self.coin_pos.append(matches['BBox'][i])
        print("there are {} cards need to pairing.".format(len(self.coin_pos)))

    def check_coins(self):
        print(self.coin_pos)
        print(len(self.coin_pos))
        while len(self.coin_pos) > 0:
            coin1_pos = self.coin_pos.pop()
            coin2_pos = self.coin_pos.pop()
            mouse_click(coin1_pos[0] + coin1_pos[2] / 2, coin1_pos[1] + coin1_pos[3] / 2,
                        wait=random.randint(2, 3) * 0.1)
            mouse_click(coin2_pos[0] + coin2_pos[2] / 2, coin2_pos[1] + coin2_pos[3] / 2,
                        wait=random.randint(3, 4) * 0.1)
            time.sleep(0.2)

            screen_shot_path = screen_grab()
            img_obj = Image.open(screen_shot_path)
            coin1_img = cropImgByRect(img_obj, wrapper_pos(coin1_pos))
            coin2_img = cropImgByRect(img_obj, wrapper_pos(coin2_pos))
            coin1_label = CoinModel.getInstance().predictSingleImg(coin1_img)
            coin2_label = CoinModel.getInstance().predictSingleImg(coin2_img)

            if coin1_label != coin2_label:
                self.coin_items[coin1_label].append(coin1_pos)
                self.coin_items[coin2_label].append(coin2_pos)
            else:
                print('.....')
                print(coin1_label)
            time.sleep(0.5)
        print(self.coin_items)

    def match_coins(self):
        for coin in self.coin_items.values():
            for c in coin:
                mouse_click(c[0] + c[2] / 2, c[1] + c[3] / 2, wait=0.2)
                time.sleep(1)
