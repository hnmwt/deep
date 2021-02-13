import  TradingView
import predict
import MT5
import time
from selenium import webdriver
import pickle
from sklearn import preprocessing
from tensorflow import keras
import pandas as pd
import numpy as np
import datetime
import os

username = 'hnmwtr999'
password = 'hnm4264wtr@'
# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
# This is the generic url that I mentioned before
#url = "https://jp.tradingview.com/chart/KQZh8MjI/#signin"
url = "https://jp.tradingview.com/chart/wznernFp/#signin"
#get_csv_dir = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview"
#train_data_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview/train_data.csv"
#get_csv_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\Intermediate\FX_GBPJPY, 30.csv"
get_csv_name = ".\FX_GBPJPY, 30.csv"

mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード
syukai_flag = False


if __name__ == '__main__':
    driver_1 = TradingView.open_browser(chromedriver_path)
    driver_2 = TradingView.site_login(username, password, url, driver_1)
    try:
        while True:
            dt_now = datetime.datetime.now()
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

#            driver_2 = TradingView.site_login(username, password, url, driver_2)
            time.sleep(6)
            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')

            time.sleep(4)
            df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
            syukai_flag, predict.pred30m = predict.pred(df, syukai_flag, predict.pred30m)
            print(str(dt_now) + '予測完了')


            #time.sleep(1200)
            time.sleep(900)
            driver_2.refresh()
            time.sleep(500)
            driver_2.refresh()
            time.sleep(395)

    except Exception as e:
        predict.Line_bot(str(dt_now) + 'エラー発生' + str(e))
        print(str(dt_now) + 'エラー発生' + str(e))