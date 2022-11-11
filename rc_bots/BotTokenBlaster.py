import time

import pyautogui

from rc_util.game_util import *
from rc_util.image_util import *
import random


class BotTokenBlaster:
    def __init__(self):
        self.start_img_path = "rc_items/games/token_blaster.png"
        self.available_moves = ["right", "left", "up", "down"]
        self.game_main_path = wrapper_img_path("rc_items/utils/game_main.png")
        self.name = "token_blaster"

    def get_name(self):
        return self.name

    def can_start(self):
        print("token blaster can play...")
        return check_image(self.start_img_path, score_threshold=0.986)

    def play(self):
        err = start_game(self.start_img_path, score_threshold=0.986)
        if err:
            return not err
        print_log_msg(self.name)
        print_log("token_blaster --> run")
        self.run_game()
        print_log("token_blaster --> finished")
        pyautogui.mouseUp()
        end_game(self.game_main_path)
        print_log("token_blaster --> end")

    def run_game(self):
        while True:
            x, y = find_image("rc_items/token_blaster/bot.png", screen_grab())
            if x is None:
                print_log("token_blaster, bot found center")
                time.sleep(1)
                x, y = find_image("rc_items/token_blaster/bot2.png", screen_grab())
                if x is None:
                    print_log("token_blaster, bot not found again")
                    if not in_game():
                        break
                    else:
                        continue
            screen = cv2.imread(screen_grab())
            bot_x, bot_y = self.get_left_bot(screen)
            bullets = self.get_bullets(screen)
            # avoid the bullet
            for b in bullets:
                bx = b[0]
                by = b[1]
                if x - 5 < bx < bot_x+5 or x + 5 > bx > bot_x - 5:
                    left_distance = y - by
                    x_distance = abs(bx - x)
                    if left_distance < x_distance * 2:
                        bot_x = x
                        bot_y = y
                if abs(bx - x) < 5:
                    bot_x = x + 50
                if abs(bot_x - x) < 5:
                    bot_x += 10
            print('x: ',x, '; y: ', y)
            print('bot_x: ',bot_x, '; bot_y: ', bot_y)

            if bot_x == -1 or bot_y == -1:
                print('not found the bot')
                continue
            else:
                pyautogui.moveTo(bot_x, bot_y)
                pyautogui.mouseDown(bot_x, bot_y)
            if not in_game():
                print("no red heart")
                break

            # if bot_x != 1150:
            #     bot_x = 1150
            # else:
            #     bot_x = 350
            # pyautogui.moveTo(bot_x, bot_y)
            # pyautogui.mouseDown(bot_x, bot_y)
            # if not in_game():
            #     print("no red heart")
            #     break
            time.sleep(2)

    def get_left_bot(self, screen):
        green_bot = "rc_items/token_blaster/green_bot.png"
        red_bot = "rc_items/token_blaster/red_bot.png"
        green = get_left_item(screen, green_bot)
        red = get_left_item(screen, red_bot)
        print('green: ',green)
        print('red: ', red)
        if green[0] == -1 and red[0] != -1:
            return red
        if green[0] != -1 and red[0] == -1:
            return green
        if green[0] == red[0] == -1:
            return -1, -1
        if green[0] < red[0]:
            return green
        return red

    def get_bullets(self, screen):
        bullet = "rc_items/token_blaster/bullet.png"
        return get_button_item(screen, bullet)


def get_left_item(screen, item):
    matches = matchTemplates(
        [("img", cv2.imread(item))],
        screen,
        N_object=float("inf"),
        score_threshold=0.8,
        searchBox=None)
    x = -1
    y = 0
    for box in matches['BBox']:
        x1 = box[0] + box[2] / 2
        y1 = box[1] + box[3] / 2
        if x1 < 346 or x1 > 1154 or y1 < 154:
            continue
        if x == -1 or x1 < x:
            x = x1
            y = y1
    return x, y


def get_button_item(screen, item):
    matches = matchTemplates(
        [("img", cv2.imread(item))],
        screen,
        N_object=float("inf"),
        score_threshold=0.8,
        searchBox=None)
    bs = []
    for box in matches['BBox']:
        x1 = box[0] + box[2] / 2
        y1 = box[1] + box[3] / 2
        if x1 < 336 or x1 > 1176:
            continue
        bs.append((x1,y1))
    return bs
