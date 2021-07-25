import base64
import time
import traceback
import cv2
import numpy as np

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from rc_util.string_util import genRandomStr

SLIDER_PADDING = 27
DISSIMILARITY_THRESHOLD = 50
CHROME_DIR = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"

CANVAS_WITH_GAP_XPATH = "//canvas[@class='geetest_canvas_bg geetest_absolute']"
CANVAS_FULL_XPATH = "//canvas[@class='geetest_canvas_fullbg geetest_fade geetest_absolute']"
SAVE_IMG_CODE = "return arguments[0].toDataURL('image/png').substring(21);"
SLIDER_BTN_CLASS_NAME = "geetest_slider_button"
RADAR_BTN_CLASS_NAME = "geetest_radar_tip"


class SliderRecaptcha(object):
    def __init__(self, url):
        self.url = url
        self.browser = webdriver.Chrome(CHROME_DIR)
        self.browser_wait_ins = WebDriverWait(self.browser, 5)

    def _extract_canvas_2_img_(self, locator, save_file=False):
        img_path = ""
        try:
            img_obj = self.browser_wait_ins.until(
                EC.presence_of_element_located((By.XPATH, locator)))
            if save_file:
                canvas_base64 = self.browser.execute_script(SAVE_IMG_CODE, img_obj)
                canvas_png = base64.b64decode(canvas_base64)
                img_path = genRandomStr() + ".png"
                with open(img_path, 'wb') as f:
                    f.write(canvas_png)
        except NoSuchElementException as ex1:
            print("there is no image in this locator -> {}".format(locator))
        except TimeoutException as ex2:
            print("there is no image in this locator -> {}".format(locator))
        except Exception as exn:
            print("There is another kind of error happened.", traceback.print_exc())
        return img_path

    def _calculate_gap_length_(self, image1_path, image2_path):
        image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
        diff = cv2.absdiff(image1, image2)
        diff[diff <= DISSIMILARITY_THRESHOLD] = 0
        return int(np.average(np.nonzero(diff)[1])) - SLIDER_PADDING

    def _generate_track_(self, distance):
        self.track = []
        first_step = int(distance / 2)
        self.track.append(first_step)
        rest = distance - first_step
        while rest > 0:
            temp_step = int(rest / 2)
            if temp_step == 0:
                break
            self.track.append(temp_step)
            rest -= temp_step
        return self.track

    def _move_slider_(self, slider):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for step in self.track:
            ActionChains(self.browser).move_by_offset(xoffset=step, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        try:
            self.browser.get(self.url)
            print("sssssssssss")

            radar_button = self.browser_wait_ins.until(
                EC.element_to_be_clickable((By.CLASS_NAME, RADAR_BTN_CLASS_NAME)))
            radar_button.click()

            canvas_with_gap_path = self._extract_canvas_2_img_(CANVAS_WITH_GAP_XPATH, True)

            if canvas_with_gap_path == "":
                print("don't need to slide the button.")
                return True
            else:
                # its time to really creak the recaptcha
                slider_button = self.browser_wait_ins.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, SLIDER_BTN_CLASS_NAME)))
                canvas_path = self._extract_canvas_2_img_(CANVAS_FULL_XPATH, True)
                gap_length = self._calculate_gap_length_(canvas_path, canvas_with_gap_path)
                print('the whole moving length is ', gap_length)
                self._generate_track_(gap_length)
                print('moving track -> ', self.track)
                self._move_slider_(slider_button)

        except Exception as e:
            print("cracking is failed.")
            self.browser.close()


recaptcha = SliderRecaptcha("https://auth.geetest.com/login/")
recaptcha.crack()
