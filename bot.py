import datetime
import os
import shutil
import rc_bots.global_var as gl

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
    gl._init()
    gl.set_value('GAME_NUM', 1)
    gl.set_value('START_TIME', datetime.datetime.now())
    setup_screen_shots_dir()
    try:
        main()
    except KeyboardInterrupt:
        print("Program closed by User!")

    finally:
        print("\nStatistics:\n",
              "Time running: {!s}\n".format(datetime.datetime.now() - gl.get_value('START_TIME')),
              "Played Games:  {!s}\n".format(gl.get_value('GAME_NUM'))
              )
        # remove all the images captured before
        shutil.rmtree('imgs')
