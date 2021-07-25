__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/24 11:37'

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_INSTALL_DIR = "D:\\Programs\\Google\\Chrome\\Application\\chrome.exe"
DEBUG_PORT = 9222
LOCALHOST = "127.0.0.1"
TEMP_DATA_DIR = "/rc_tmp"
START_UP_SH = CHROME_INSTALL_DIR + " --remote-debugging-port=" + str(DEBUG_PORT)

print(START_UP_SH)
os.system(START_UP_SH)

options = Options()
options.add_argument("user-data-dir=" + TEMP_DATA_DIR)
options.add_experimental_option("debuggerAddress", LOCALHOST + ":" + str(DEBUG_PORT))

driver = webdriver.Chrome(options=options, executable_path="../rc_ext/chromedriver-91.0.4472.exe")
executor_url = driver.command_executor._url
session_id = driver.session_id
print(session_id)
print(executor_url)
driver.get("http://www.spiderpy.cn/")
