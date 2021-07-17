__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/17 17:18'


from rc_util.game_util import find_image, check_image


screen_path = "../imgs/full_snap__1626483257.png"
recaptha_path = "../rc_items/utils/recaptha1.png"


res = find_image(recaptha_path, screen_path)
print(res)
