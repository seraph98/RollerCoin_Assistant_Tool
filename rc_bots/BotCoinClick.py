from rc_util.game_util import *
from rc_util.image_util import *
from threading import Thread


class BotCoinClick:
    def __init__(self):
        self.start_img_path = "rc_items/games/coinclick.png"
        self.name = "CoinClick"
        self.game_status = "idle"

    def can_start(self):
        return check_image(self.start_img_path)

    def play(self):
        err = start_game(self.start_img_path)
        if err:
            return not err
        print_log_msg(self.name)
        self.run_game()
        end_game(self.start_img_path)

    def run_game(self):
        self.game_status = "running"
        # try:
            # thread = ThreadWithReturnValue(target=check_image,
                                           # args=("rc_items/gain_power.png", True, self,))
            # thread.start()
        # except:
            # print("Unable to start thread for checking image")
            # end_game(self.start_img_path)

        x1 = 400 
        y1 = 250 
        x2 = 1128 
        y2 = 680 
        while self.game_status == "running":
            if check_image("rc_items/utils/restart.png"):
                self.game_status = "ended"
                print("break....")
                break
            print('......')
            pic = pyautogui.screenshot(region=(x1, y1, x2, y2,))
            width, height = pic.size
            clicked = False
            for x in range(0, width, 5):
                if clicked:
                    print("clicked!!!!!!!")
                    break
                for y in range(0, height, 5):
                    r, g, b, _ = pic.getpixel((x, y))

                    # blue coin
                    if b == 183 and r == 0:
                        mouse_click(x + x1, y + y1 + 10, wait=0)
                        clicked = True
                        break

                    # yellow coin
                    elif b == 64 and r == 200:
                        clicked = True
                        mouse_click(x + x1, y + y1 + 10, wait=0)
                        break

                    # orange coin
                    elif b == 33 and r == 231:
                        clicked = True
                        mouse_click(x + x1, y + y1 + 10, wait=0)
                        break

                    # grey coin
                    elif b == 230 and r == 230:
                        clicked = True
                        mouse_click(x + x1, y + y1 + 10, wait=0)
                        break

                    if self.game_status == "ended":
                        break
                if self.game_status == "ended":
                    break




class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
