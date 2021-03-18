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
import pandas as pd
import backtest_variable
backtest = backtest_variable.backtest

username = 'hnmwtr999'
password = 'hnm4264wtr@'
# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード
DF = pd.DataFrame()
url = "https://jp.tradingview.com/chart/lXaj0SrK/#signin"
get_csv_name = r".\OANDA_USDJPY, 5.csv"
if backtest == True:
    get_csv_name = r".\OANDA_USDJPY, 5_test.csv"

csv_time = 5
symbol = "USDJPY"#"GBPJPY"
model_dir = '.\model'
scalar_dir = '.\dump'
lot = 0.1  # ロット数



def MACD_Cross_judge(Cross_judge, order, tp_point):
    if Cross_judge == 9:
        pass
    elif Cross_judge == 0:  # 買いシグナル
        order = MT5.NARIYUKI_BUY
        tp_point = 20
#        Line_bot("買いシグナル")
    elif Cross_judge == 1:  # 売りシグナル
        order = MT5.NARIYUKI_SELL
        tp_point = 20
#        Line_bot("売りシグナル")
    return order ,tp_point

def EA(bktest_orbit=0):
    try:
#        while True:
        dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
        if backtest == False:  # バックテストがTrueならcsvは削除しない
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

            time.sleep(2)
            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')
            time.sleep(4)

        df, MACD, MACD_signal, MACD_Cross = predict.create_train_data(get_csv_name, bktest_orbit)  # 取ってきたcsvからdfを作成
        predict.syukai_flag, predict.pred30m, diff, pred_after_time = predict.pred(df, predict.syukai_flag, predict.pred30m, csv_time, model_dir, scalar_dir,bktest_orbit)  # 値を予測
        MACD_judge, Cross_judge = predict.MACD_sign(MACD, MACD_signal, MACD_Cross)
        lot = 0.1  # ロット数

        if backtest == True:  # バックテスト
            tp_point = MT5.backtest_tp
            sl_point = MT5.backtest_sl
        elif backtest == False:  # 本番
            tp_point = 20
            sl_point = 1

        # 予測値が一定以上の場合→買い注文
        if 0.12 <= float(diff) and MACD_judge == MT5.NARIYUKI_BUY:
            order = MT5.NARIYUKI_BUY  # 指値買い注文
        #    sl_point = 40
        #    tp_point = 50
            magic = 234000
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "買い注文"

        # 予測値が一定以上の場合→買い注文(少)
        elif 0.02 < float(diff) < 0.12 and MACD_judge == MT5.NARIYUKI_BUY:
            order = MT5.NARIYUKI_BUY  # 指値買い注文
           # sl_point = 70
            #tp_point = 30
            magic = 234001
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "買い注文(少)"

        # 予測値が一定以上の場合→買い注文(少)
        elif 0 <= float(diff) <= 0.02 and MACD_judge == MT5.NARIYUKI_BUY:
            order = MT5.NARIYUKI_BUY  # 指値買い注文
          #  sl_point = 70
            magic = 234001
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "買い注文(極少)"

        # 予測値が一定以下の場合→売り注文
        elif float(diff) <= -0.12 and MACD_judge == MT5.NARIYUKI_SELL:
            order = MT5.NARIYUKI_SELL  # 指値売り注文
        #    sl_point = 40
        #    tp_point = 50
            magic = 235000
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "売り注文"

        # 予測値が一定以下の場合→売り注文(少)
        elif -0.12 < float(diff) < -0.02 and MACD_judge == MT5.NARIYUKI_SELL:
            order = MT5.NARIYUKI_SELL  # 指値売り注文
           # sl_point = 70
           # tp_point = 30
            magic = 235000
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "売り注文(少)"

        # 予測値が一定以下の場合→売り注文(少)
        elif -0.02 <= float(diff) < 0 and MACD_judge == MT5.NARIYUKI_SELL:
            order = MT5.NARIYUKI_SELL  # 指値売り注文
          #  sl_point = 70
            magic = 235000
            order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
            MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
            order_name = "売り注文(極少)"



        # 予測値が条件に当てはまらないとき
        else:
            order = MT5.NARIYUKI_SELL  # 指値売り注文
            lot = 0 # ロット数
            sl_point = 0
            tp_point = 0
            magic = 000000
            if backtest == True: # バックテストの時のみ下記の処理に入る
                MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df,order_flag=False)
            order_name = "注文無し"

        message = str(dt_now) + \
        '\n予測時刻:' + str(pred_after_time) + \
        '\n予測値:' + str(predict.pred30m) + \
        '\n前回予測との差額:' + str(diff) + \
        '\nオーダー:' + str(order_name)

        print(message)
        if backtest == False: # 本番
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
        if backtest == False:  # 本番
            Line_bot("エラー発生" + str(tb))

def work_interval_30m():
    minute = 30  # minuteの間隔で動作
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

def work_interval_15m():
    # 15分毎のjob実行を登録
    dt_now = datetime.datetime.now()  # 現在時刻
    dt_now_criteria_00m = dt_now.replace(minute=0, second=0)  # 基準時刻
    dt_now_criteria_15m = dt_now.replace(minute=15, second=0) # 基準時刻
    dt_now_criteria_30m = dt_now.replace(minute=30, second=0)  # 基準時刻
    dt_now_criteria_45m = dt_now.replace(minute=45, second=0)  # 基準時刻

    # 現在時刻(分)が0以上15未満
    if dt_now_criteria_00m <= dt_now < dt_now_criteria_15m:
        job_start_time = dt_now_criteria_15m  # ジョブスタート時間は30分
    # 現在時刻(分)が15以上30未満
    elif dt_now_criteria_15m <= dt_now < dt_now_criteria_30m:
        job_start_time = dt_now_criteria_30m  # ジョブスタート時間は30分
    # 現在時刻(分)が30以上45未満
    elif dt_now_criteria_30m <= dt_now < dt_now_criteria_45m:
        job_start_time = dt_now_criteria_45m  # ジョブスタート時間は30分
    # 現在時刻(分)が45以上
    elif dt_now_criteria_45m <= dt_now:
        job_start_time = dt_now + datetime.timedelta(hours=1)  # ジョブスタート時間を1時間後にする # ジョブスタート時間は30分
        job_start_time = job_start_time.replace(minute=0, second=0)
    return job_start_time

def work_interval_5m():
    # 15分毎のjob実行を登録
    dt_now = datetime.datetime.now()  # 現在時刻
    dt_now_criteria_00m = dt_now.replace(minute=0, second=0)  # 基準時刻
    dt_now_criteria_05m = dt_now.replace(minute=5, second=0)  # 基準時刻
    dt_now_criteria_10m = dt_now.replace(minute=10, second=0)  # 基準時刻
    dt_now_criteria_15m = dt_now.replace(minute=15, second=0) # 基準時刻
    dt_now_criteria_20m = dt_now.replace(minute=20, second=0)  # 基準時刻
    dt_now_criteria_25m = dt_now.replace(minute=25, second=0)  # 基準時刻
    dt_now_criteria_30m = dt_now.replace(minute=30, second=0)  # 基準時刻
    dt_now_criteria_35m = dt_now.replace(minute=35, second=0)  # 基準時刻
    dt_now_criteria_40m = dt_now.replace(minute=40, second=0)  # 基準時刻
    dt_now_criteria_45m = dt_now.replace(minute=45, second=0)  # 基準時刻
    dt_now_criteria_50m = dt_now.replace(minute=50, second=0)  # 基準時刻
    dt_now_criteria_55m = dt_now.replace(minute=55, second=0)  # 基準時刻

    if dt_now_criteria_00m <= dt_now < dt_now_criteria_05m:
        job_start_time = dt_now_criteria_05m  # ジョブスタート時間は30分

    elif dt_now_criteria_05m <= dt_now < dt_now_criteria_10m:
        job_start_time = dt_now_criteria_10m  # ジョブスタート時間は30分

    elif dt_now_criteria_10m <= dt_now < dt_now_criteria_15m:
        job_start_time = dt_now_criteria_15m  # ジョブスタート時間は30分

    elif dt_now_criteria_15m <= dt_now < dt_now_criteria_20m:
        job_start_time = dt_now_criteria_20m  # ジョブスタート時間は30分

    elif dt_now_criteria_20m <= dt_now < dt_now_criteria_25m:
        job_start_time = dt_now_criteria_25m  # ジョブスタート時間は30分

    elif dt_now_criteria_25m <= dt_now < dt_now_criteria_30m:
        job_start_time = dt_now_criteria_30m  # ジョブスタート時間は30分

    elif dt_now_criteria_30m <= dt_now < dt_now_criteria_35m:
        job_start_time = dt_now_criteria_35m  # ジョブスタート時間は30分

    elif dt_now_criteria_35m <= dt_now < dt_now_criteria_40m:
        job_start_time = dt_now_criteria_40m  # ジョブスタート時間は30分

    elif dt_now_criteria_40m <= dt_now < dt_now_criteria_45m:
        job_start_time = dt_now_criteria_45m  # ジョブスタート時間は30分

    elif dt_now_criteria_45m <= dt_now < dt_now_criteria_50m:
        job_start_time = dt_now_criteria_50m  # ジョブスタート時間は30分

    elif dt_now_criteria_50m <= dt_now < dt_now_criteria_55m:
        job_start_time = dt_now_criteria_55m  # ジョブスタート時間は30分

    elif dt_now_criteria_55m <= dt_now:
        job_start_time = dt_now + datetime.timedelta(hours=1)  # ジョブスタート時間を1時間後にする # ジョブスタート時間は30分
        job_start_time = job_start_time.replace(minute=0, second=0)

    return job_start_time

if __name__ == '__main__':

    if backtest == False:  # 本番
    #    job_start_time = work_interval_30m()
    #    job_start_time = work_interval_15m()
        job_start_time = work_interval_5m()

        # 初回
        driver_1 = TradingView.open_browser(chromedriver_path)
        driver_2 = TradingView.site_login(username, password, url, driver_1)
        EA(0)
        print("次回時刻" + str(job_start_time))

        # 2回目以降
        while True:
            if job_start_time <= datetime.datetime.now():  # 指定時間 <= 現在時刻の時に処理をスタートする
                EA()
    #            job_start_time = work_interval_30m()  # 処理終了後に指定時間を更新する
    #            job_start_time = work_interval_15m()
                job_start_time = work_interval_5m()
                print("次回時刻" + str(job_start_time))
            time.sleep(1)



    elif backtest == True:  # バックテスト
        if os.path.isfile(MT5.backtest_log):
            os.remove(MT5.backtest_log)
            with open(MT5.backtest_log, mode="a", encoding="shift_jis")as f:
                f.write("売買した時刻," + "利益," + "0が買い注文、1が売り注文," + "tp," + "sl," + "現時点の買い価格(buy)," +
                        "現時点の売り価格(sell)," + "high注文後~," + "low注文後~," + "\n")
        print('バックテスト')
      #  for i in range(915 ,1200):
        for i in range(1853, 3530):
            EA(i)
        print('**************終了***********************')
        print('総計',MT5.profit_all)
        print('ポジション持ち越し回数',MT5.carryover_position)
