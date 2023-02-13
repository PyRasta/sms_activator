import json
import time
import random
import glob

import requests
from requests.auth import HTTPDigestAuth
from get_driver import get_driver
from selenium.webdriver.common.by import By
from onlinesimru import Driver
import multiprocessing

AUTH = HTTPDigestAuth(username='rasta', password='6516599')
SERVER_URL = 'http://bezrabotnyi.com:8888'
API_KEY = 'B2hzW8hu3bA7Rxj-3E2hpnpf-F77s48gk-9UnGNn6E-a9ydk839JXNg216'


def get_random_proxies():
    proxies = requests.get(f'{SERVER_URL}/proxy/', auth=AUTH, timeout=15).json()
    proxy = random.choice(proxies)
    proxy = proxy['proxy']
    return proxy


def submit_code(driver_sms, number, tzid):
    driver = False
    while not driver:
        try:
            proxy = get_random_proxies()
            driver = get_driver(proxy)
        except:
            driver = False
    if driver:
        driver.get('https://yappy.media/auth')
        input_number = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div/div[1]/form/div[2]/input')
        input_number.send_keys(number)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div/div[1]/button').click()
        print(f'7{number}')
        try:
            code = driver_sms.numbers().wait_code(tzid)
            inputs = driver.find_elements(By.TAG_NAME, 'input')
            for i, c in zip(inputs, code):
                i.send_keys(c)
            time.sleep(10)
            with open(f'cookies/cookies7{number}.pkl', 'w') as file:
                json.dump(driver.get_cookies(), file)
            driver.close()
        except:
            print('bad number')
            driver.close()


def get_len_cookies():
    return len(glob.glob('cookies/*'))


def get_cookie(need_len_cookies):
    driver = Driver(API_KEY)
    try:
        balance_dict = driver.user().balance()
        balance = balance_dict['balance']
    except Exception as error:
        balance = False
        print(error)
    if balance:
        while get_len_cookies() <= need_len_cookies or float(balance) <= 5:
            number_dict = driver.numbers().get(service='Yappy', number=True)
            number = number_dict['number'][2:]
            submit_code(driver, number, number_dict['tzid'])
            try:
                balance_dict = driver.user().balance()
                balance = balance_dict['balance']
            except Exception as error:
                print(error)
                exit()


def main(need_len_cookies):
    processes = 5
    for i in range(0, processes):
        multiprocessing.Process(target=get_cookie, args=(need_len_cookies,)).start()

