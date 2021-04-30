import TradingView
import predict
import MT5
import MetaTrader5 as mt5
import time
from sklearn import preprocessing
import datetime
import os
import sys
import traceback
from Line_bot import Line_bot
from Line_bot import Line_bot_error
#import schedule
import pandas as pd
import backtest_variable
import param
import order_stop
import algorithm
import req
import Indicator

backtest = backtest_variable.backtest
up_down_identifers_list_100_10 = []#order_stop.up_down_identifers_list_400_200
up_down_identifers_list_200_100 = []#order_stop.up_down_identifers_list_200_100
up_down_identifers_list_400_200 = []#order_stop.up_down_identifers_list_400_200
up_down_identifers_list_300_200 = []#order_stop.up_down_identifers_list_400_200
up_down_identifers_list_500_400 = []#order_stop.up_down_identifers_list_400_200
up_down_identifers_list_600_500 = []#order_stop.up_down_identifers_list_400_200
syukai_flag = predict.syukai_flag
pred_close = predict.pred_close
pred_high = predict.pred_high
pred_low = predict.pred_low

status_ago_M15 = Indicator.status_ago_M15
status_now_M15 = Indicator.status_now_M15
change_status_M15 = Indicator.change_status_M15

status_ago_M5 = Indicator.status_ago_M5
status_now_M5 = Indicator.status_now_M5
change_status_M5 = Indicator.change_status_M5


username = 'hnmwtr999'
password = 'hnm4264wtr@'
# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード
DF = pd.DataFrame()
url = "https://jp.tradingview.com/chart/BtgoDHOz/#signin"
get_csv_name = r".\OANDA_USDJPY, 15.csv"
#get_csv_name = r".\OANDA_USDJPY, 5.csv"  # 5分足
if backtest == True:
#    get_csv_name = r".\OANDA_USDJPY, 5_test.csv"  # 5分足
    get_csv_name = r".\OANDA_USDJPY, 15_test.csv"

#csv_time = 5
csv_time = 15  # 15min
symbol = param.symbol
model_dir = '.\model'
scalar_dir = '.\dump'
lot = param.lot  # ロット数


def calc_ATR(df):
    ATR = df["ATR"]
    ATR_last = ATR[-1:]  # 最終行を抜き出し
    ATR_value = ATR_last * 3 *1000
    return float(ATR_value)

def MACD_Cross_judge(Cross_judge, order, tp_point):  # macdによるシグナル発生で注文を強制的に変更
    if Cross_judge == 9:
        pass
    elif Cross_judge == 0:  # 買いシグナル
        order = MT5.NARIYUKI_BUY
        tp_point = 40
#        Line_bot("買いシグナル")
    elif Cross_judge == 1:  # 売りシグナル
        order = MT5.NARIYUKI_SELL
        tp_point = 40
#        Line_bot("売りシグナル")
    return order, tp_point

def EA(bktest_orbit=0):
    try:
#        while True:
        dt_now = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')
        if backtest == False:  # バックテストがTrueならcsvは削除しない
            # 前回のcsvがあるとき削除
            if os.path.isfile(get_csv_name):
                os.remove(get_csv_name)

            TradingView.get_csv(driver_2)
            print('csvファイルダウンロード完了')
            time.sleep(3)

        lot = 0.1  # ロット数

        df, MACD, MACD_signal, MACD_Cross = predict.create_train_data(get_csv_name, bktest_orbit)  # 取ってきたcsvからdfを作成

        global syukai_flag
        global pred_close
        global pred_high
        global pred_low

        syukai_flag, pred_close, diff_close, pred_high, diff_high, pred_low, diff_low, pred_after_time =\
            predict.summarize(df, syukai_flag, pred_close, pred_high, pred_low, csv_time, bktest_orbit)  # 値を予測

        MACD_judge, Cross_judge = predict.MACD_sign(MACD, MACD_signal, MACD_Cross)  # MACDの判定
#        predict.VOLUME_judge(df, tp_point, sl_point)

        volume = df["Volume"]  # カラム抜き出し
        volume_ma = df["Volume MA"]  # カラム抜き出し
        volume_last = volume[-1:]  # 最終行を抜き出し
        volume_ma_last = volume_ma[-1:] # 最終行を抜き出し
        volume_last =volume_last.to_numpy()  # ifで計算するためnumpyに変換
        volume_ma_last =volume_ma_last.to_numpy()  # ifで計算するためnumpyに変換
        if volume_last < (volume_ma_last * 10):  # 取引量 < 平均取引量  追加21.04.10
   #     if True:  # 追加21.04.10


            if backtest == True:  # バックテスト
                tp_point = MT5.backtest_tp
                sl_point = MT5.backtest_sl
                sl_point = calc_ATR(df)
            elif backtest == False:  # 本番
                tp_point = 80
        #     sl_point = 100
                sl_point = calc_ATR(df)

            # 予測値が一定以上の場合→買い注文(少)
            if 0 < float(diff_close):# and 0 < float(diff_high) and 0 < float(diff_low):# and MACD_judge == MT5.NARIYUKI_BUY:
                order = MT5.NARIYUKI_BUY  # 指値買い注文
              #  sl_point = 70
                magic = 234000
                order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
                MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
                order_name = "買い注文"

            # 予測値が一定以下の場合→売り注文(少)
            elif float(diff_close) < 0 :#and float(diff_high) < 0 and float(diff_low) < 0:# and MACD_judge == MT5.NARIYUKI_SELL:
                order = MT5.NARIYUKI_SELL  # 指値売り注文
              #  sl_point = 70
                magic = 235000
                order, tp_point = MACD_Cross_judge(Cross_judge, order, tp_point)
                MT5.order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df)
                order_name = "売り注文"

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

        else:
            print(dt_now,":取引量が大きいので売買無し")
            order_name = "注文無し"
    
        message = str(dt_now) + \
        '\n予測時刻:' + str(pred_after_time) + \
        '\n予測値 close:' + str(pred_close) + 'high:' + str(pred_high) + 'low:' + str(pred_low) +\
        '\n前回予測との差額 close:' + str(diff_close) + 'high:' + str(diff_high) + 'low:' + str(diff_low) +\
        '\nオーダー:' + str(order_name) + \
        '\nMACD_judge:' + str(MACD_judge) + "・0がbuy・1がsell"


        print(message)
        #if backtest == True: # 本番

        # ログ書き込み
        today = datetime.datetime.today().strftime("%Y%m%d")
        if backtest == True:  # バックテストの時は名前を変える
            log_name = today + "バックテスト.csv"
        elif backtest == False:
            log_name = today + ".csv"
        log_name = "./注文log/" + log_name

        if not os.path.isfile(log_name): # ログファイルが無い時はヘッダーを書き込む
            with open(log_name, mode="a", encoding="shift_jis") as head:
                header = "現在時刻,予測時刻,オーダー,予測値,MACD_judge,現在価格,tp,sl\n"
                head.write(header)

        with open(log_name, mode="a", encoding="shift_jis") as f:  # ログ内容書き込み
            log = str(dt_now) + ',' + str(pred_after_time) + ',' + str(order_name) + ',' + str(pred_close) + ',' + str(MACD_judge) + ',' + \
                  str(MT5.log_price) + ',' + str(MT5.log_tp) + ',' + str(MT5.log_sl)
            f.write(log + "\n")

        Line_bot(message)

#        time.sleep(980)
#        driver_2.refresh()
#        #time.sleep(860)
#        time.sleep(802)
       # driver_2.refresh()

    except Exception as e:
        t, v, tb = sys.exc_info()
        message = traceback.print_tb(tb)
        print(message, t, v)
        if backtest == False:  # 本番
            Line_bot_error("エラー発生" + str(message))

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
        act = 0
        # 初回
        if param.EA == True:   # フラグがtrueの時にtradingview→AI予測を行う
            driver_1 = TradingView.open_browser(chromedriver_path)
            driver_2 = TradingView.site_login(username, password, url, driver_1)
            EA(0)
            print("次回時刻" + str(job_start_time))

            today = datetime.datetime.today().strftime("%Y%m%d")
            today = today + ".csv"
            log_name = "./注文log/" + today
            with open(log_name, mode="a", encoding="utf-8") as f:
                f.write("取引開始")

        mt5.initialize()
        authorized = mt5.login(param.account_ID, password=param.password)  # ログイン
        order_stop.min1_price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 ※askは朝方スプレッドが広がるためbidにする
        ichimoku_tp_15M = 0.1
        ichimoku_tp_5M = 0.04
        status_ago_M15, status_now_M15, change_status_M15 = Indicator.ichimoku_order(mt5.TIMEFRAME_M15, status_ago_M15,
                                                                                     status_now_M15, change_status_M15, ichimoku_tp_15M)
        status_ago_M5, status_now_M5, change_status_M5 = Indicator.ichimoku_order(mt5.TIMEFRAME_M5, status_ago_M5,
                                                                                    status_now_M5, change_status_M5, ichimoku_tp_5M)

        algorithm.range_price()

# 2回目以降
        count = 0
        while True:
            dt_now = datetime.datetime.now()
            if job_start_time <= dt_now:  # 指定時間 <= 現在時刻の時に処理をスタートする
                print('*******START*******')
                time.sleep(1)
                count += 1
            #    algorithm.force_settlement()  # 一定時間以上経っているとき強制決済
                if count == 3:
                    status_ago_M15, status_now_M15, change_status_M15 = Indicator.ichimoku_order(mt5.TIMEFRAME_M15,
                                                                                         status_ago_M15,
                                                                                         status_now_M15,
                                                                                         change_status_M15, ichimoku_tp_15M)
                    algorithm.range_price()  # アルゴリズムによる自動売買
                    count = 0

                status_ago_M5, status_now_M5, change_status_M5 = Indicator.ichimoku_order(mt5.TIMEFRAME_M5, status_ago_M5,
                                                                                      status_now_M5, change_status_M5, ichimoku_tp_5M)



                if param.EA == True:      # フラグがtrueの時にtradingview→AI予測を行う 
                    EA()

               # job_start_time = work_interval_30m()  # 処理終了後に指定時間を更新する
               # job_start_time = work_interval_15m()
                job_start_time = work_interval_5m()
                print("次回時刻" + str(job_start_time))

            if act % 2 == 0:   #  余りが0の時 (10カウントに一度処理を行う(約10秒?))
                positions = mt5.positions_get(symbol=symbol)
                #     up_down_identifers_list_600_500 = order_stop.order_up_down_settle(positions,up_down_identifers_list_600_500, 600,500)
                #     up_down_identifers_list_500_400 = order_stop.order_up_down_settle(positions,up_down_identifers_list_500_400, 500,400)
                #    up_down_identifers_list_400_200 = order_stop.order_up_down_settle(positions,up_down_identifers_list_400_200, 400,300)
                #    up_down_identifers_list_300_200 = order_stop.order_up_down_settle(positions,up_down_identifers_list_300_200, 300,200)
                #    up_down_identifers_list_200_100 = order_stop.order_up_down_settle(positions, up_down_identifers_list_200_100, 200, 100)
           #     up_down_identifers_list_100_10 = order_stop.order_up_down_settle(positions,up_down_identifers_list_100_10, 100,10)
                algorithm.settlement(1)

            if act % 60 == 0: #  余りが0の時 (60カウントに一度処理を行う(約40秒?))
            #    order_stop.rapid_change(positions)
                act = 0  # カウンタ初期化

                # 1日に一度だけ注文する
                if dt_now.hour == param.day_of_order_time_hour:
                    if dt_now.minute == param.day_of_order_time_minute:
                        magic = 999999
                        value = 0.1
                        comment = "day_of_one_buy"
                        price = mt5.symbol_info_tick(symbol).ask
                        req.normal_request(req.Buy, price, magic, comment, value)  # 新規注文(買い)
                        comment = "day_of_one_sell"
                        price = mt5.symbol_info_tick(symbol).bid
                        req.normal_request(req.Sell, price, magic, comment, value)  # 新規注文(売り)

            act += 1
            time.sleep(1)



    elif backtest == True:  # バックテスト
#        if os.path.isfile(MT5.backtest_log):
#            os.remove(MT5.backtest_log)
        with open(MT5.backtest_log, mode="a", encoding="shift_jis")as f:
            #f.write("予測値tp:" + str(MT5.backtest_tp) + "予測値sl:" + str(MT5.backtest_sl) + "\n")
            f.write("売買した時刻," + "利益," + "0が買い注文、1が売り注文," + "tp," + "sl," + "現時点の買い価格(buy)," +
                    "現時点の売り価格(sell)," + "high注文後~5分後まで," + "low注文後~5分後まで," + "総利益," +
                    "予測値tp:" + str(MT5.backtest_tp) + "予測値sl:" + str(MT5.backtest_sl) + "\n")
        print('バックテスト')
      #  for i in range(915 ,1200):
        for i in range(50, 1080):
            EA(i)
        print('**************終了***********************')
        print('総計',MT5.profit_all)
        print('ポジション持ち越し回数',MT5.carryover_position)
