import  TradingView
import predict
import time
from selenium import webdriver
import pickle
from sklearn import preprocessing
from tensorflow import keras
import pandas as pd
import numpy as np
import os

username = 'hnmwtr999'
password = 'hnm4264wtr@'
# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
# This is the generic url that I mentioned before
url = "https://jp.tradingview.com/chart/KQZh8MjI/#signin"
#get_csv_dir = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview"
#train_data_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview/train_data.csv"
#get_csv_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\Intermediate\FX_GBPJPY, 60.csv"
get_csv_name = ".\FX_GBPJPY, 60.csv"

mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード

if __name__ == '__main__':
    driver_1 = TradingView.open_browser(chromedriver_path)
    driver_2 = TradingView.site_login(username, password, url, driver_1)

    while True:
        # 前回のcsvがあるとき削除
        if os.path.isfile(get_csv_name):
            os.remove(get_csv_name)

#        driver_2 = TradingView.site_login(username, password, url, driver_2)
        time.sleep(6)
        TradingView.get_csv(driver_2)
        print('csvファイルダウンロード完了')

        time.sleep(4)
        df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
        predict.pred(df)  # 1-24時間後まで予測
        print('予測完了')
        time.sleep(1790)