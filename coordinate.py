import datetime, os, time, json

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException


def click_sele_(driver, row):
    try:
        khungtimkiem = driver.find_element(By.XPATH, '//form[@data-e2e="search-box"]//input')
    except Exception as e:
        input("""khungtimkiem = driver.find_element(By.XPATH, '//form[@data-e2e="search-box"]//input')""")
        khungtimkiem = driver.find_element(By.XPATH, '//form[@data-e2e="search-box"]//input')
    try:
        khungtimkiem.send_keys(row)
    except ElementNotInteractableException:
        khungtimkiem_ = driver.find_element(By.XPATH,
                                            '//button[@aria-label="Search"]//div[@class="TUXButton-iconContainer"]')
        khungtimkiem_.click()  # driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        khungtimkiem = driver.find_elements(By.XPATH, '//form[@data-e2e="search-box"]//input[@placeholder="Search"]')
        try:
            khungtimkiem[0].send_keys(row)
        except NoSuchElementException:
            khungtimkiem[1].send_keys(row)

    khungtimkiem.send_keys(Keys.RETURN)


def click_sele(driver, row):
    sp = row.split(' ')
    link = f'https://www.tiktok.com/search?q={"%20".join(sp)}'
    driver.get(link)
    time.sleep(2)


def readfile(file="uid.txt", mod="r", cont=None, jso: bool = False):
    if not mod in ("w", "a", ):
        assert os.path.isfile(file), str(file)
    if mod == "r":
        with open(file, encoding="utf-8") as file:
            lines: list = file.readlines()
        return lines
    elif mod == "_r":
        with open(file, encoding="utf-8") as file:
            contents = file.read() if not jso else json.load(file)
        return contents
    elif mod == "rb":
        with open(file, mod) as file:
            contents = file.read()
        return contents
    elif mod in ("w", "a", ):
        with open(file, mod, encoding="utf-8") as fil_e:
            if not jso:
                fil_e.write(cont)
            else:
                json.dump(cont, fil_e, indent=2, ensure_ascii=False)

# (1887, 3015) (2387, 3015) (2417, 3015) (2444, 3015)
# (3544, 4015) (3015, 4015) (3096, 4015) (3125, 4015)
# (0, 1000) (500, 1500) (528, 1500) (566, 1500)
