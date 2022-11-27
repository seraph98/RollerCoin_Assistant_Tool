from rc_util.game_util import *
from rc_util.image_util import *
from threading import Thread


class BotCoinClick:
    def __init__(self):
        self.start_img_path = "rc_items/games/coinclick.png"
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "CoinClick"

    def get_name(self):
        return self.name

    def can_start(self):
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return err
        print_log_msg(self.name)
        print_log("coin_match --> run")
        self.run_game()
        print_log("coin_match --> finished")
        end_game(self.game_main_path)
        print_log("coin_match --> end")

    def run_game(self):
        x1 = 320
        y1 = 270
        width = 860
        height = 440
        i = 0
        while True:
            if not check_image("rc_items/utils/score_coinclick.png"):
                print_log("break....")
                break
            pic = pyautogui.screenshot(region=(x1, y1, width, height,))
            width, height = pic.size
            print_log("-------"+str(i)+"----")
            i += 1
            for x in range(0, width, 15):
                for y in range(0, height, 15):
                    matched = False
                    r, g, b = pic.getpixel((x, y))
                    # blue coin
                    if (r == 0 and g == 96 and b == 158) or (r == 0 and g == 116 and b == 183) \
                            or (r == 0 and g == 116 and b == 184) \
                            or (r == 1 and g == 119 and b == 187):
                        matched = True
                        print("blue coin click")

                    # yellow coin
                    if match_color(r,g,b, [(183, 153, 56), (220, 189, 89), (226, 191, 73),
                                           (200, 168, 63), (249, 243, 220),(200, 168, 64),
                                            (226, 191, 75)]):
                        print("yellow coin click")
                        matched = True

                        # orange coin
                    if match_color(r, g, b, [(249, 224, 199),
                            (255, 152, 49),
                            (255, 153, 49),
                            (251, 150, 46),
                            (231, 131, 33)]):
                        matched = True
                        print("orange coin click")

                    # grey coin
                    if r == 230 and b == 230 or r == g == b == 224 \
                            or r == g == b == 141:
                        print("grey coin click")
                        matched = True
                    if matched:
                        print("[rgb]: ", r, ",", g, ",", b)
                        pyautogui.click(x + x1, y + y1 + 15)
                        # for xx in range(x-5, x+5):
                        #     for yy in range(y+10, y+20):
                        #         pic.putpixel((xx, yy), (255, 0, 0))
            # pic.save("test_"+str(i)+".png")

def match_color(r, g, b, candidates):
    for c in candidates:
        if r == c[0] and g == c[1] and b == c[2]:
            return True
    return False
