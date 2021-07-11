__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:30'

from PIL import Image

from rc_bots.game_util import *
from rc_bots.image_util import *


class BotCoinFlipBot:
    def __init__(self):
        self.game_img_path = "rc_items/games/coinflip_gameimg.png"
        self.game = "CoinFlip"
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
        self.coin_images = [
            ("binance", cv2.imread("rc_items/coinflip/coinflip_item_binance.png")),
            ("btc", cv2.imread("rc_items/coinflip/coinflip_item_btc.png")),
            ("eth", cv2.imread("rc_items/coinflip/coinflip_item_eth.png")),
            ("litecoin", cv2.imread("rc_items/coinflip/coinflip_item_litecoin.png")),
            ("monero", cv2.imread("rc_items/coinflip/coinflip_item_monero.png")),
            ("eos", cv2.imread("rc_items/coinflip/coinflip_item_eos.png")),
            ("rlt", cv2.imread("rc_items/coinflip/coinflip_item_rlt.png")),
            ("xrp", cv2.imread("rc_items/coinflip/coinflip_item_xrp.png")),
            ("xml", cv2.imread("rc_items/coinflip/coinflip_item_xml.png")),
            ("tether", cv2.imread("rc_items/coinflip/coinflip_item_tether.png")),
        ]

    def can_start(self):
        return check_image(self.game_img_path)

    def play(self):
        start_game(self.game_img_path)
        print_log_msg(self.game)
        # get all coin position and the amount
        self.get_coin_fields()
        self.check_coins()
        self.match_coins()
        end_game()

    def get_coin_fields(self):
        screen = cv2.imread(screen_grab())
        matches = matchTemplates(
            [("card", cv2.imread("rc_items/coinflip/coinflip_back.png"))],
            screen,
            N_object=float("inf"),
            score_threshold=0.5,
            searchBox=None)
        for i in range(len(matches['BBox'])):
            self.coin_pos.append(matches['BBox'][i])
        print("there are {} cards need to pairing.".format(len(self.coin_pos)))

    def check_coins(self):
        while len(self.coin_pos) > 0:
            coin1_pos = self.coin_pos.pop()
            coin2_pos = self.coin_pos.pop()
            mouse_click(coin1_pos[0] + coin1_pos[2] / 2, coin1_pos[1] + coin1_pos[3] / 2, wait=0.1)
            mouse_click(coin2_pos[0] + coin2_pos[2] / 2, coin2_pos[1] + coin2_pos[3] / 2, wait=0.1)
            time.sleep(0.2)
            screen_shot_path = screen_grab()
            screen = cv2.imread(screen_shot_path)
            img_obj = Image.open(screen_shot_path)
            cropImgByRect(img_obj, wrapper_pos(coin1_pos), True)
            cropImgByRect(img_obj, wrapper_pos(coin2_pos), True)
            # first version using matchTemplates to classify the image
            matches = matchTemplates(
                self.coin_images,
                screen,
                N_object=2,
                score_threshold=.7,
                maxOverlap=.25,
                searchBox=None).values.tolist()

            print("matches -> ", matches)
            coin1_name = None
            for result in matches:
                # result sample -> ['btc', (908, 245, 116, 118), 0.8617702722549438]
                if coin1_name is not None and result[0] == coin1_name:
                    # if two coin are matched, we dont need to saved their positions
                    self.coin_items[coin1_name] = []
                else:
                    if coin1_name is None:
                        coin1_name = result[0]
                    self.coin_items[result[0]].append(result[1])

            if len(matches) == 0:
                self.coin_pos.append(coin1_pos)
                self.coin_pos.append(coin2_pos)
                continue

            # if len(matches) == 1:
            #     # if we only recognize one, we can add another unrecognized pos into next turn
            #     different_pos = find_a_dissimilar(matches[0][1], coin1_pos, coin2_pos)
            #     self.coin_pos.append(different_pos)

    def match_coins(self):
        for coin in self.coin_items.values():
            if len(coin) == 2:
                c1 = coin[0]
                mouse_click(c1[0] + c1[2] / 2, c1[1] + c1[3] / 2, wait=0.05)
                c2 = coin[1]
                mouse_click(c2[0] + c2[2] / 2, c2[1] + c2[3] / 2, wait=0.05)
                time.sleep(0.75)
