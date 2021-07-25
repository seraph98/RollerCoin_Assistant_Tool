import datetime
import os
import shutil

import rc_util.global_var as global_var
from rc_bots.BotCoinFlipBot import BotCoinFlipBot


def setup_screen_shots_dir():
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    else:
        shutil.rmtree('imgs')
        os.mkdir('imgs')


def main():
    Bots = [BotCoinFlipBot]
    while True:
        for bot in Bots:
            if bot().can_start():
                bot().play()


if __name__ == "__main__":
    # check the url TODO
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
