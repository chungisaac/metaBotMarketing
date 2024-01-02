import os
import time

import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CWD = os.getcwd()
OLD_FOLDER_NAME = 'folder_upTill202309110221'
FOLDER_NAME = 'folder_new'

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=chrome_options)


def get_screenshot(browser, id, url, wait_time):
    filename = f"{FOLDER_NAME}/{id}.png"
    old_filename = f"{OLD_FOLDER_NAME}/{id}.png"

    if os.path.exists(os.path.join(CWD, filename)) or os.path.exists(os.path.join(CWD, old_filename)):
        return
    browser.get(url)
    time.sleep(wait_time)
    browser.get_screenshot_as_file(filename)


def main():
    df = pd.read_csv("links.csv")
    for i, row in tqdm(df.iterrows(), total=len(df)):
        wait_time = 4 if i == 0 else 2
        get_screenshot(browser, row['id'], row['text'], wait_time)


if __name__ == '__main__':
    main()



# from html2image import Html2Image
# hti = Html2Image()
# hti.browser.flags = ['--default-background-color=000000', '--hide-scrollbars', '--block-new-web-contents', '--allow-http-screen-capture']
# hti.screenshot(url='https://www.facebook.com/permalink.php?story_fbid=122117887592019276&id=61550578292223', save_as='123.png')
