import datetime
import os
import shutil
import time

import pyautogui
import argparse
from rc_mail.mail import sendMail

import rc_util.global_var as global_var
from rc_bots.BotTokenBlaster import BotTokenBlaster
from rc_bots.BotCoinClick import BotCoinClick
from rc_bots.BotCoinMatch import BotCoinMatch
from rc_bots.BotFlappyRocket import  BotFlappyRocket

from rc_bots.Bot2048 import Bot2048

from rc_bots.BotCoinFlipBot import BotCoinFlipBot


def setup_screen_shots_dir():
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    else:
        shutil.rmtree('imgs')
        os.mkdir('imgs')


def main():
    # Bots = [BotCoinFlipBot]
    # Bots = [Bot2048]
    # Bots = [BotTokenBlaster]
    Bots = [BotCoinMatch]
    # Bots = [BotCoinFlipBot, Bot2048, BotTokenBlaster, BotFlappyRocket, BotCoinMatch, BotCoinClick]
    # Bots = [BotFlappyRocket]
    i = 1
    validation = {
        'hku': 0,
        '229': 0
    }
    not_play_count = {
        'hku': 0,
        '229': 0
    }
    current = '229'
    while True:
        if i % 2 == 0:
            current = 'hku'
            pyautogui.click(35, 390) # google
            time.sleep(2)
        else:
            current = '229'
            pyautogui.click(35, 453) # google
            time.sleep(2)

        # for scrolling, need to click first
        pyautogui.click(152, 426)
        if not_play_count[current] >= 30:
            not_play_count[current] = 0
            sendMail("rollercoin", current + ": not play count is  over 30, refresh the page")
            pyautogui.press('f5')
            shutil.rmtree('imgs')
            setup_screen_shots_dir()
            time.sleep(10)
        i += 1
        ts = int(time.time())
        if validation[current] > ts:
            time.sleep(3)
            continue
        not_play_count[current] += 1
        for bot in Bots:
            pyautogui.scroll(100)
            print('main: scroll 100')
            print('main: ', bot().get_name())
            if bot().get_name() == 'enter_the_chainers':
                print('main: scroll -100')
                pyautogui.scroll(-100)
            else:
                print('main: scroll -5')
                pyautogui.scroll(-5)
            time.sleep(2)
            print("start....", bot().get_name())
            if bot().can_start():
                not_play_count[current] = 0
                print(bot().get_name(), 'can start')
                try:
                    result = bot().play()
                    if result == "validation":
                        sendMail("rollercoin", current + ": need validation and try again")
                        h = time.localtime().tm_hour
                        if h > 23:
                            validation[current] = int(time.time()) + 600
                        elif h < 10:
                            validation[current] = int(time.time()) + 3600
                        else:
                            validation[current] = int(time.time()) + 300
                        break
                    if result == "retry":
                        sendMail("rollercoin", current + ": retry")
                        pyautogui.press('f5')
                        time.sleep(10)
                except Exception as e:
                    print(bot().get_name(), ': ', e)
                    pyautogui.press('f5')


if __name__ == "__main__":
    # check the url TODO
    time.sleep(3)
    global_var.init()
    setup_screen_shots_dir()
    try:
        main()
    except KeyboardInterrupt:
        print("Program closed by User!")

    finally:
        print("\nStatistics:\n",
              "Time running: {!s}\n".format(datetime.datetime.now() - global_var.get_value('START_TIME')),
              "Played Games:  {!s}\n".format(global_var.get_value('GAME_NUM'))
              )
        # remove all the images captured before
        shutil.rmtree('imgs')
