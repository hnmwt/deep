from bs4 import BeautifulSoup
import requests
import time
import selenium.webdriver
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import random
import datetime

#**********************グローバル宣言********************
TRIAUTO_LOGIN_URL = 'https://mypage.invast.jp/portal/login/'
DRIVER = webdriver.Chrome()
LOGIN_ID = 'hnmwtr927@gmail.com'
PASSWORD = 'hnm4264wtr'
#**********************グローバル宣言********************

class TRIAUTO_TRADE_Remove():
    DRIVER.get(TRIAUTO_LOGIN_URL)  # ログインページに遷移
    # 変数宣言
    id = DRIVER.find_element_by_css_selector('#contents_full > div.inv_box_login_form > div > form > div:nth-child(1) > input[type=text]')
    password = DRIVER.find_element_by_css_selector('#contents_full > div.inv_box_login_form > div > form > div:nth-child(2) > input[type=password]')
    login_button = DRIVER.find_element_by_css_selector('#contents_full > div.inv_box_login_form > div > form > div.col-btn > input')

    # ログイン⇒マイページに遷移まで
    time.sleep(1)
    id.send_keys(LOGIN_ID)  # IDを入力
    password.send_keys(PASSWORD)  # PASSWORDを入力
    login_button.click()  # ログインボタンをクリックしてマイページに遷移
    time.sleep(5)

    # マイページに遷移後⇒トライオートホーム画面に遷移まで
    Mypage_Triauto_button = DRIVER.find_element_by_css_selector('#menu_right > div:nth-child(6) > div:nth-child(1)')
    Mypage_Triauto_button.click()  # トライオートホーム画面に遷移
    time.sleep(10)
    handle_array = DRIVER.window_handles  # ウィンドウハンドルを取得する
    DRIVER.switch_to.window(handle_array[1])  # seleniumで操作可能なdriverを切り替える

    # トライオートホーム画面に遷移後⇒トライオートトレード画面に遷移まで
    Mypage_Triauto_Trade_button = DRIVER.find_element_by_css_selector('#root > div.routingComponent_wrapper__1cj86 > div.sideBar_wrapper__1OPGF.routingComponent_sidebar__2VHBm > div > a:nth-child(2)')
    Mypage_Triauto_Trade_button.click()  # トライオートトレード画面に遷移


    