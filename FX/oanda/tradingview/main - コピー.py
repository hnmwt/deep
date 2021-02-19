import  TradingView
import predict
import MT5
import time
from sklearn import preprocessing
import datetime
import os
import sys
import traceback
from Line_bot import Line_bot
import schedule

username = 'hnmwtr999'
password = 'hnm4264wtr@'
# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
url = "https://jp.tradingview.com/chart/wznernFp/#signin"
get_csv_name = ".\FX_GBPJPY, 30.csv"
mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード

syukai_flag = False  # 周回フラグ

def job():
    driver_1 = TradingView.open_browser(chromedriver_path)
    driver_2 = TradingView.site_login(username, password, url, driver_1)
    try:
        while True:
            dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

            time.sleep(6)
            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')

            time.sleep(4)
            df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
            syukai_flag, predict.pred30m, diff_30m, pred_after_time = predict.pred(df, syukai_flag, predict.pred30m)  # 値を予測

            # 予測値が一定以上の場合→買い注文
            if 0.12 < float(diff_30m):
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - float(0.05)  #  リミット価格は予測-0.05
                order = MT5.NARIYUKI_BUY  # 指値買い注文
                MT5.order(order, limit_rate, lot)
                order_name = "買い注文"

            # 予測値が一定以下の場合→売り注文
            elif float(diff_30m) < -0.12:
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - float(0.05)  # リミットかか木は予想-0.05
                order = MT5.NARIYUKI_SELL  # 指値売り注文
                MT5.order(order, limit_rate, lot)
                order_name = "売り注文"

            # 予測値が売り、買い条件に当てはまらないとき
            else:
                order_name = "注文無し"

            message = str(dt_now) + \
            '\n予測時刻:' + str(pred_after_time) + \
            '\n予測値:' + str(predict.pred30m) + \
            '\n前回との差額:' + str(diff_30m) + \
            '\nオーダー:' + str(order_name)

            print(message)
            Line_bot(message)

            time.sleep(980)
            driver_2.refresh()
            #time.sleep(860)
            time.sleep(802)
           # driver_2.refresh()

if __name__ == '__main__':
    driver_1 = TradingView.open_browser(chromedriver_path)
    driver_2 = TradingView.site_login(username, password, url, driver_1)
    try:
        while True:
            dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

            time.sleep(6)
            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')

            time.sleep(4)
            df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
            syukai_flag, predict.pred30m, diff_30m, pred_after_time = predict.pred(df, syukai_flag, predict.pred30m)  # 値を予測

            # 予測値が一定以上の場合→買い注文
            if 0.12 < float(diff_30m):
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - float(0.05)  #  リミット価格は予測-0.05
                order = MT5.NARIYUKI_BUY  # 指値買い注文
                MT5.order(order, limit_rate, lot)
                order_name = "買い注文"

            # 予測値が一定以下の場合→売り注文
            elif float(diff_30m) < -0.12:
                lot = 0.1  # ロット数
                limit_rate = predict.pred30m - float(0.05)  # リミットかか木は予想-0.05
                order = MT5.NARIYUKI_SELL  # 指値売り注文
                MT5.order(order, limit_rate, lot)
                order_name = "売り注文"

            # 予測値が売り、買い条件に当てはまらないとき
            else:
                order_name = "注文無し"

            message = str(dt_now) + \
            '\n予測時刻:' + str(pred_after_time) + \
            '\n予測値:' + str(predict.pred30m) + \
            '\n前回との差額:' + str(diff_30m) + \
            '\nオーダー:' + str(order_name)

            print(message)
            Line_bot(message)

            time.sleep(980)
            driver_2.refresh()
            #time.sleep(860)
            time.sleep(802)
           # driver_2.refresh()

            while datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S') == '%Y/%m/%d/ %H:%30:%S':

                # 30分毎のjob実行を登録
                dt_now = datetime.datetime.now()  # 現在時刻
                dt_now_criteria = dt_now.replace(minute=30) # 基準時刻
                dt_diff = dt_now - dt_now_criteria  # 現在時刻と基準時刻の差
                dt_diff_sec = dt_diff.total_seconds()  # 秒数変換

                # 現在時刻(分)が30分より前
                if dt_diff_sec < 0:
                    job_start_time = dt_now_criteria  # ジョブスタート時間は30分

                # 現在時刻(分)が30分以降(30分含む)
                elif 0 <= dt_diff_sec:
                    hour = dt_now.hour
                    job_start_time = dt_now.replace(hour=hour+1,minute=0,second=0)  # ジョブスタート時間は時間が繰り上がった後

                job_start_time_fmt = job_start_time.strftime('%H:%M')

                # ジョブスタート時間のjob実行を登録
                schedule.every().day.at(job_start_time_fmt).do(job)#jobがおわったらjob_notstart_flagをfalseにする処理を追加する
                                                                   #flagがfalseならジョブを廃棄する処理を追加
                job_notstart_flag = True
                while job_notstart_flag == True:
                    schedule.run_pending()
                    time.sleep(1)

                while True:
                    schedule.every(30).minutes.do(job)

    except Exception as e:
        t, v, tb = sys.exc_info()
        message = traceback.print_tb(tb)
        print(message, t, v)
        Line_bot("エラー発生" + str(tb))
      #  predict.Line_bot(str(dt_now) + 'エラー発生' + str(e))
      #  print(str(dt_now) + 'エラー発生' + str(e))