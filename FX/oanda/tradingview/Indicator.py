import datetime
import MetaTrader5 as mt5
import pandas as pd
import req
import param
import time

# 現在の最大表示列数の出力
pd.get_option("display.max_columns")

# 最大表示列数の指定（ここでは50列を指定）
pd.set_option('display.max_columns', 50)

status_ago = 9
status_now = 9
change_status = 9


def ichimoku_order():
    global status_ago
    global status_now
    global change_status

    mt5.initialize()
    rates = mt5.copy_rates_from_pos("USDJPY", mt5.TIMEFRAME_M15, 0, 78)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')  # unix→標準
    df["time"] = df["time"] + pd.tseries.offsets.Hour(6)  # 6時間後
    #print(df)

    df_9 = df.iloc[-9:-1]
    days9_high = df_9['high'].max()
    days9_low = df_9['low'].min()
    tenkan = (days9_high + days9_low) / 2  # 転換線
    #print("転換線：", tenkan)

    df_26 = df.iloc[-26:-1]
    days26_high = df_26['high'].max()
    days26_low = df_26['low'].min()
    kijun = (days26_high + days26_low) / 2  # 基準線
    #print("基準線：", kijun)


    df_35_to_26 = df[42:51]
    df_35_to_26_high = df_35_to_26['high'].max()
    df_35_to_26_low = df_35_to_26['high'].min()
    tenkan_span1 = (df_35_to_26_high + df_35_to_26_low) /2

    df_52_to_26 =  df[25:51]
    df_52_to_26_high = df_52_to_26['high'].max()
    df_52_to_26_low = df_52_to_26['high'].min()
    kijun_span1 = (df_52_to_26_high + df_52_to_26_low) / 2

    senkou_span1 = (tenkan_span1 + kijun_span1) / 2  # 先行スパン1
    #print("先行スパン1：", senkou_span1)

    df_52 = df[0:51]
    days52_high = df_52['high'].max()
    days52_low = df_52['low'].min()
    senkou_span2 = (days52_high + days52_low) / 2  # 先行スパン2
    #print("先行スパン2：", senkou_span2)


    tien_span = df['close'].iloc[-1]  # 遅延スパン
    print("転換線：", tenkan, ",基準線：", kijun, ",先行スパン1：", senkou_span1, ",先行スパン2：", senkou_span2, ",遅延スパン：", tien_span)


    if kijun < tenkan:  # 転換線が基準線より上の場合
        status_now = req.Buy
    elif tenkan < kijun:  # 転換線が基準線より下の場合
        status_now = req.Sell

    if status_ago == 0 and status_now == 1:  # 転換線が基準線を下抜けしたとき(売り注文)
        change_status = req.Sell
        print('転換線が基準線を下抜け')
    elif status_ago == 1 and status_now == 0:  # 転換線が基準線を上抜けしたとき(買い注文)
        change_status = req.Buy
        print('転換線が基準線を上抜け')
    else:  # 当てはまらないとき
        change_status = 9

    status_ago = status_now  # 計算終了後statusを変数に格納する

    if change_status == req.Sell:
        settle_type = change_status
        price = mt5.symbol_info_tick(symbol).bid
        magic = 999999
        value = 0.5
        comment = "ichimoku_sell"
        req.normal_request(settle_type, price, magic, comment, value)
    elif change_status == req.Buy:
        settle_type = change_status
        price = mt5.symbol_info_tick(symbol).ask
        magic = 999999
        value = 0.5
        comment = "ichimoku_buy"
        req.normal_request(settle_type, price, magic, comment, value)




