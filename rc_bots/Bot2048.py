from rc_util.game_util import *
from rc_util.image_util import *
import random

class Bot2048:
    def __init__(self):
        self.start_img_path = "rc_items/games/2048_gameimg.png"
        self.available_moves = ["right", "left", "up", "down"]
        self.name = "2048"

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
        while True:
            x, y = find_image("rc_items/2048/center.png", screen_grab())
            if x is None:
                break
            for _ in range(10):
                action = random.choice(self.available_moves) 
                if action == "right":
                    mouse_move_right(x,y,100)
                if action == "left":
                    mouse_move_left(x,y,100)
                if action == "up":
                    mouse_move_up(x,y,100)
                if action == "down":
                    mouse_move_down(x,y,100)
                time.sleep(0.2)
