__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 10:30'

from rc_bots.util import *


class BotCoinFlipBot:
    def __init__(self):
        self.start_img_path = "rc_items/games/coinflip_gameimg.png"
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
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return False
        start_game_msg(self.game)
        self.get_coin_fields()
        self.check_coins()
        self.match_coins()
        end_game()
        return True

    def get_coin_fields(self):
        screen = cv2.imread(screen_grab())
        matches = matchTemplates(
            [("card", cv2.imread("rc_items/coinflip/coinflip_back.png"))],
            screen,
            N_object=float("inf"),
            score_threshold=0.5,
            # maxOverlap=0.25,
            searchBox=None)
        for i in range(len(matches['BBox'])):
            self.coin_pos.append(matches['BBox'][i])
        print(self.coin_pos)

    def check_coins(self):
        ind = 0
        max_index = len(self.coin_pos)
        while ind < max_index:
            coin1_pos = self.coin_pos[ind]
            coin2_pos = self.coin_pos[ind + 1]

            mouse_click(coin1_pos[0] + coin1_pos[2] / 2, coin1_pos[1] + coin1_pos[3] / 2, wait=0.1)
            mouse_click(coin2_pos[0] + coin2_pos[2] / 2, coin2_pos[1] + coin2_pos[3] / 2, wait=0.3)
            screen = cv2.imread(screen_grab())
            matches = matchTemplates(
                self.coin_images,
                screen,
                N_object=2,
                score_threshold=.7,
                maxOverlap=.25,
                searchBox=None)

            try:

                coin1 = (matches["TemplateName"][0], matches["BBox"][0])
                coin2 = (matches["TemplateName"][1], matches["BBox"][1])
                print("coin1: {}, coin2: {}".format(coin1, coin2))

                if coin1[0] == coin2[0]:
                    self.coin_items.pop(coin1[0])
                else:
                    self.coin_items[coin1[0]].append(coin1[1])
                    self.coin_items[coin2[0]].append(coin2[1])

                ind += 2
            except KeyError:
                print("maybe match failed in someway")
            except IndexError:
                # TODO
                print("maybe need to restart game")

    def match_coins(self):
        for coin in self.coin_items.values():
            if len(coin) == 2:
                c1 = coin[0]
                mouse_click(c1[0] + c1[2] / 2, c1[1] + c1[3] / 2, wait=0.05)
                c2 = coin[1]
                mouse_click(c2[0] + c2[2] / 2, c2[1] + c2[3] / 2, wait=0.05)
                time.sleep(1)
