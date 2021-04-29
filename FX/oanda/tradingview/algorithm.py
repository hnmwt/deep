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

sell = 1
buy = 0
symbol = param.symbol
trend_flag = False
occurrence_trend_date = '0'
order_trend_type = 9


def Spread(spread):
    if spread[-2] <= 3:
        return True


# パターン１売り注文
def Sell(open, close, high, low, spread, value):
    if close[-5] < close[-4]:
        if close[-2] < close[-3] < close[-4]:
            if Spread(spread) == True:
                settle_type = sell
                price = mt5.symbol_info_tick(symbol).bid
                magic = 555555
                comment = "pat1_sell"
                req.normal_request(settle_type, price, magic, comment, value)
                return True


# 条件変更(4点判定から3点判定)→momとほぼ同じため使わない
def Sell_0428(open, close, high, low, spread, value):
    if close[-4] < close[-3]:
        if close[-2] < close[-3]:
            if Spread(spread) == True:
                settle_type = sell
                price = mt5.symbol_info_tick(symbol).bid
                magic = 555555
                comment = "pat1_sell"
                req.normal_request(settle_type, price, magic, comment, value)
                return True


# パターン１買い注文
def Buy(open, close, high, low, spread, value):
    if close[-4] < close[-5]:
        if close[-4] < close[-3] < close[-2]:
            if Spread(spread) == True:
                settle_type = buy
                price = mt5.symbol_info_tick(symbol).ask
                magic = 555555
                comment = "pat1_buy"
                req.normal_request(settle_type, price, magic, comment, value)
                return True


# 条件変更(4点判定から3点判定)→momとほぼ同じため使わない
def Buy_0428(open, close, high, low, spread, value):
    if close[-3] < close[-4]:
        if close[-3] < close[-2]:
            if Spread(spread) == True:
                settle_type = buy
                price = mt5.symbol_info_tick(symbol).ask
                magic = 555555
                comment = "pat1_buy"
                req.normal_request(settle_type, price, magic, comment, value)
                return True


# パターン2売り注文(勢いがあるとき(highとopenが近い))
def mom_Sell(open, close, high, low, spread, value):
    settle_type = sell
    if close[-4] < close[-3]:
        if close[-2] < close[-3]:
            # if high[-2] - open[-2] <= 0.005:
            if True == calc_mom(open, close, high, low, settle_type):
                if Spread(spread) == True:
                    price = mt5.symbol_info_tick(symbol).bid
                    magic = 555555
                    comment = "pat2_mom_sell"
                    req.normal_request(settle_type, price, magic, comment, value)
                    return True


# high_lowに占めるopen_closeの割合が大きいか確かめる関数(勢いの見極め)
def calc_mom(open, close, high, low, settle_type):
    percentage = 10  # しきい値
    high_percentage = 100  # 初期値
    low_percentage = 100  # 初期値

    open_close = abs(open[-2] - close[-2])
    high_low = abs(high[-2] - low[-2])
    if settle_type == buy:
        open_low = abs(open[-2] - low[-2])
        close_high = abs(close[-2] - high[-2])
        high_percentage = close_high / high_low * 100
        low_percentage = open_low / high_low * 100

    elif settle_type == sell:
        open_high = abs(open[-2] - high[-2])
        close_low = abs(close[-2] - low[-2])
        high_percentage = open_high / high_low * 100
        low_percentage = close_low / high_low * 100

    if high_percentage < percentage and low_percentage < percentage:
        return True


# パターン2買い注文(勢いがあるとき(lowとopenが近い))
def mom_Buy(open, close, high, low, spread, value):
    settle_type = buy
    if close[-3] < close[-4]:
        if close[-3] < close[-2]:
            #  if open[-2] - low[-2] <= 0.005:
            if True == calc_mom(open, close, high, low, settle_type):
                if Spread(spread) == True:
                    price = mt5.symbol_info_tick(symbol).ask
                    magic = 555555
                    comment = "pat2_mom_buy"
                    req.normal_request(settle_type, price, magic, comment, value)
                    return True


# パターン3 トレンド発生時に一度だけ注文を行う
def order_trend(open, close, spread, value, time):
    if trend_flag:
        if occurrence_trend_date == time[-2]:
            if Spread(spread):
                settle_type = order_trend_type
                price = mt5.symbol_info_tick(symbol).ask
                magic = 666666
                comment = "trend"
                req.normal_request(settle_type, price, magic, comment, value)
                return True


# トレンド発生判断
def judge_trend(time, close):
    global trend_flag
    global occurrence_trend_date
    global order_trend_type

    if close[-5] < close[-4] < close[-3] < close[-2]:
        if not trend_flag:
            trend_flag = True
            occurrence_trend_date = time[-2]
            order_trend_type = req.Buy
    elif close[-2] < close[-3] < close[-4] < close[-5]:
        if not trend_flag:
            trend_flag = True
            occurrence_trend_date = time[-2]
            order_trend_type = req.Sell
    else:
        trend_flag = False
    print('trend_flag:',trend_flag)
       # occurrence_trend_date = time[-2]


# 決済処理
def settlement(order_type):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        for position in positions:
            identifier = position[7]  # 保有ポジションの識別子
            price = position[13]  # 価格
            position_type = position[5]  # オーダータイプ
            magic = position[6]  # マジックナンバー
            profit = position[15]  # 利益
            comment = "range_settlement"

            #    if position_type != order_type:  # 保有ポジションのタイプとこれからオーダーするポジションのタイプがダブらないようにする
            if 600 < profit:
                print("position_type;", position_type)
                print("order_type:", order_type)
                if position_type == buy and magic == 555555:
                    settle_type = sell  # 送信するオーダータイプ
                #      req.settlement_request(settle_type, price, magic, comment, identifier)
                elif position_type == sell and magic == 555555:
                    settle_type = buy  # 送信するオーダータイプ
            #       req.settlement_request(settle_type, price, magic, comment, identifier)


# ポジションを一定時間保有している場合に強制的に決済する
def force_settlement():
    mt5.initialize()
    positions = mt5.positions_get(symbol=symbol)
    for position in positions:
        unix_time_utc = position[1]  # 注文時刻
        magic = position[6]  # マジックナンバー
        normal_time_utc = datetime.datetime.fromtimestamp(unix_time_utc)  # ポジションの注文時刻(ロンドン時間)
        normal_time_jst = normal_time_utc + datetime.timedelta(hours=9)  # ポジションの注文時刻(日本時間)
        dt_now = datetime.datetime.now()  # 現在時刻
        diff_time_day = dt_now.day - normal_time_jst.day  # 日付の差
        diff_time_hour = dt_now.hour - normal_time_jst.hour  # 時間の差
        #print(diff_time_day)
        #print(diff_time_hour)
        if 2 <= diff_time_hour:  # 保有時間が1時間を過ぎている場合に決済
            if magic != 999999:
                position_type = position[5]  # オーダータイプ
                identifier = position[7]  # 保有ポジションの識別子
                price = position[13]  # 価格
                position_type = position[5]  # オーダータイプ
                profit = position[15]  # 利益
                comment = "1hour_over"

                if position_type == buy:
                    settle_type = sell  # 送信するオーダータイプ
                    req.settlement_request(settle_type, price, magic, comment, identifier)
                elif position_type == sell:
                    settle_type = buy  # 送信するオーダータイプ
                    req.settlement_request(settle_type, price, magic, comment, identifier)


def range_price():
    import time
    time.sleep(1)
    value = 0.04

    mt5.initialize()
    dt_now = datetime.datetime.now()
    time_from = dt_now - datetime.timedelta(hours=9)  # 3時間前の東京時間
    time_to = dt_now  # - datetime.timedelta(hours=6) # 3時間前の東京時間
    # 2020.01.10 00:00-2020.01.11 13:00 UTCでUSDJPY M15からバーを取得する
    #   rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, time_from, time_to)
    rates = mt5.copy_rates_from_pos("USDJPY", mt5.TIMEFRAME_M15, 0, 20)
    df = pd.DataFrame(rates)

    df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')  # unix→標準
    df["time"] = df["time"] + pd.tseries.offsets.Hour(6)  # 6時間後

    print(df)
    #    print(df["close"])
    time = df['time'].tolist()
    open = df["open"].tolist()
    close = df["close"].tolist()
    high = df["high"].tolist()
    low = df["low"].tolist()
    spread = df["spread"].tolist()

    order_flag = False

    judge_trend(time, close)

    if Sell(open, close, high, low, spread, value):
    #if Sell_0428(open, close, high, low, spread, value):  # 4点判定から3点判定
        settlement(Sell)
        print('Sell')
        order_flag = True
    if Buy(open, close, high, low, spread, value):
    #if Buy_0428(open, close, high, low, spread, value):  # 4点判定から3点判定
        settlement(Buy)
        print('Buy')
        order_flag = True
    if mom_Sell(open, close, high, low, spread, value):
        settlement(Sell)
        print('mom_Sell')
        order_flag = True
    if mom_Buy(open, close, high, low, spread, value):
        settlement(Buy)
        print('mom_Buy')
        order_flag = True
    if order_trend(open, close, spread, value, time):
        print('trend')
        order_flag = True

    if order_flag == False:
        print("レンジ帯：該当のパターン無し")




if __name__ == '__main__':
    #   settlement()
    #   range_price()
    force_settlement()