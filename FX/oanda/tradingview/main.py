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
import sys
import traceback
from Line_bot import Line_bot

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
            dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

#            driver_2 = TradingView.site_login(username, password, url, driver_2)
            time.sleep(6)
            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')

            time.sleep(4)
            df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
            syukai_flag, predict.pred30m, diff_30m, pred_after_time = predict.pred(df, syukai_flag, predict.pred30m)  # 値を予測

            # 予測値が一定以上の場合→買い注文
            if 0.2 < diff_30m:
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - 0.05  #  リミット価格は予測-0.05
                order = MT5.NARIYUKI_SASINE_BUY  # 指値買い注文
                MT5.order(order, limit_rate, lot)
                message_title = "買い注文"

            # 予測値が一定以下の場合→売り注文
            elif diff_30m < -0.2:
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - 0.05  # リミットかか木は予想-0.05
                order = MT5.NARIYUKI_SASINE_SELL  # 指値売り注文
                MT5.order(order, limit_rate, lot)
                message_title = "売り注文"

            # 予測値が売り、買い条件に当てはまらないとき
            else:
                message_title = "注文無し"

            message = str(dt_now) + \
            '\n予測時刻:' + str(pred_after_time) + \
            '\n予測値:' + str(predict.pred30m) + \
            '\n前回との差額:' + str(diff_30m) + \
            '\nオーダー:' + str(message_title)

            print(message)
            Line_bot(message)

            time.sleep(900)
            driver_2.refresh()
            time.sleep(500)
           # driver_2.refresh()
            time.sleep(395)

    except Exception as e:
        t, v, tb = sys.exc_info()
        message = traceback.print_tb(tb)
        print(message)
        Line_bot(message)
      #  predict.Line_bot(str(dt_now) + 'エラー発生' + str(e))
      #  print(str(dt_now) + 'エラー発生' + str(e))