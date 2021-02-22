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
minute = 30 #minuteの間隔で動作


def EA():
    symbol = "GBPJPY"
    try:
#        while True:
        dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
        # 前回のcsvがあるとき削除
        if os.path.isfile(get_csv_name):
            os.remove(get_csv_name)

        time.sleep(6)
        TradingView.get_csv(driver_2)
        print('csvファイルダウンロード完了')

        time.sleep(4)
        df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
        predict.syukai_flag, predict.pred30m, diff_30m, pred_after_time = predict.pred(df, predict.syukai_flag, predict.pred30m)  # 値を予測

        # 予測値が一定以上の場合→買い注文
        if 0.12 <= float(diff_30m):
            lot = 0.14  # ロット数
            sl_point = 1000
            tp_point = 100
            magic = 234000
            order = MT5.NARIYUKI_BUY  # 指値買い注文
            MT5.order(order, sl_point,tp_point, lot, magic, symbol)
            order_name = "買い注文"

        # 予測値が一定以上の場合→買い注文(少)
        elif 0.06 < float(diff_30m) < 0.12:
            lot = 0.14  # ロット数
            sl_point = 700
            tp_point = 30
            magic = 234001
            order = MT5.NARIYUKI_BUY  # 指値買い注文
            MT5.order(order, sl_point,tp_point, lot, magic, symbol)
            order_name = "買い注文(少)"

        # 予測値が一定以下の場合→売り注文
        elif float(diff_30m) <= -0.12:
            lot = 0.14  # ロット数
            sl_point = 700
            tp_point = 100
            magic = 235000
            order = MT5.NARIYUKI_SELL  # 指値売り注文
            MT5.order(order, sl_point,tp_point, lot, magic, symbol)
            order_name = "売り注文"

        # 予測値が一定以下の場合→売り注文(少)
        elif -0.12 < float(diff_30m) < -0.06:
            lot = 0.14  # ロット数
            sl_point = 1000
            tp_point = 30
            magic = 235000
            order = MT5.NARIYUKI_SELL  # 指値売り注文
            MT5.order(order, sl_point,tp_point, lot, magic, symbol)
            order_name = "売り注文(少)"

        # 予測値が条件に当てはまらないとき
        else:
            order_name = "注文無し"

        message = str(dt_now) + \
        '\n予測時刻:' + str(pred_after_time) + \
        '\n予測値:' + str(predict.pred30m) + \
        '\n前回予測との差額:' + str(diff_30m) + \
        '\nオーダー:' + str(order_name)

        print(message)
        Line_bot(message)

#            time.sleep(980)
#            driver_2.refresh()
#            #time.sleep(860)
#            time.sleep(802)
           # driver_2.refresh()

    except Exception as e:
        t, v, tb = sys.exc_info()
        message = traceback.print_tb(tb)
        print(message, t, v)
        Line_bot("エラー発生" + str(tb))

def work_interval():
    # 30分毎のjob実行を登録
    dt_now = datetime.datetime.now()  # 現在時刻
    dt_now_criteria = dt_now.replace(minute=minute, second=0) # 基準時刻
    dt_diff = dt_now - dt_now_criteria  # 現在時刻と基準時刻の差
    dt_diff_sec = dt_diff.total_seconds()  # 秒数変換

    # 現在時刻(分)が30分より前 → 30分にスタート
    if dt_diff_sec < 0:
        job_start_time = dt_now_criteria  # ジョブスタート時間は30分

    # 現在時刻(分)が30分以降(30分含む)→次の00分にスタート
    elif 0 <= dt_diff_sec:
        job_start_time = dt_now + datetime.timedelta(hours=1)  # ジョブスタート時間を1時間後にする
        job_start_time = job_start_time.replace(minute=0,second=0)  # ジョブスタート時間の分秒を0にする
    return job_start_time


if __name__ == '__main__':

    job_start_time = work_interval()

    # 初回
    driver_1 = TradingView.open_browser(chromedriver_path)
    driver_2 = TradingView.site_login(username, password, url, driver_1)
    EA()
    print("次回時刻" + str(job_start_time))
 #   # ジョブの登録 & 現在時刻が指定の時間になるまで待機
 #   print('ジョブスタート時間:', job_start_time)
 #   while job_start_time > datetime.datetime.now():
 #       time.sleep(1)
 #   schedule.every(minute).minutes.do(job)
 #   print('ジョブ登録完了')
 #   job()  # ループを抜けたら2回目のジョブを実行(ここで時間補正を行う)
 #
 #   # 2回目以降は指定した時間毎に処理を行う
 #   while True:
 #       schedule.run_pending()
 #       time.sleep(1)

    # 2回目以降
    while True:
        if job_start_time <= datetime.datetime.now():  # 指定時間 <= 現在時刻の時に処理をスタートする
            EA()
            job_start_time = work_interval()  # 処理終了後に指定時間を更新する
            print("次回時刻" + str(job_start_time))
        time.sleep(10)