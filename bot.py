import datetime
import os
import shutil
import time

import pyautogui
import argparse

import rc_util.global_var as global_var
from rc_bots.BotTokenBlaster import BotTokenBlaster
from rc_bots.BotEnterTheChainers import  BotEnterTheChainers

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
    Bots = [BotCoinFlipBot, Bot2048, BotTokenBlaster]
    i = 0
    while True:
        if i >= 10:
            i = 0
            pyautogui.press('f5')
            time.sleep(10)
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
            print("start....", i)
            i += 1
            if bot().can_start():
                print(bot().get_name(), 'can start')
                i = 0
                try:
                    bot().play()
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
