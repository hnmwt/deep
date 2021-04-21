import datetime
import MetaTrader5 as mt5
import pandas as pd
import req
import param
import time

#現在の最大表示列数の出力
pd.get_option("display.max_columns")

#最大表示列数の指定（ここでは50列を指定）
pd.set_option('display.max_columns', 50)

sell = 1
buy = 0
symbol = param.symbol

def Spread(spread):
    if spread[-1] <= 3:
        return True

# パターン１売り注文
def Sell(open, close, high, low, spread):
    if close[-4] < close[-3]:
        if close[-1] < close[-2] < close[-3]:
            if Spread(spread) == True:
                settle_type = sell
                price =  mt5.symbol_info_tick(symbol).bid
                magic = 555555
                comment = "pat1_sell"
                req.normal_request(settle_type, price, magic, comment)
                return True

# パターン１買い注文
def Buy(open, close, high, low, spread):
    if close[-3] < close[-4]:
        if close[-3] < close[-2] < close[-1]:
            if Spread(spread) == True:
                settle_type = buy
                price =  mt5.symbol_info_tick(symbol).ask
                magic = 555555
                comment = "pat1_buy"
                req.normal_request(settle_type, price, magic, comment)
                return True

# パターン2売り注文(勢いがあるとき)
def mom_Sell(open, close, high, low, spread):
    if close[-3] < close[-2]:
        if close[-1] < close[-2]:
            if high[-1] - open[-1] <= 0.005:
                if Spread(spread) == True:
                    settle_type = sell
                    price = mt5.symbol_info_tick(symbol).bid
                    magic = 555555
                    comment = "pat2_mom_sell"
                    req.normal_request(settle_type, price, magic, comment)
                    return True

# パターン2買い注文(勢いがあるとき)
def mom_Buy(open, close, high, low, spread):
    if close[-2] < close[-3]:
        if close[-2] < close[-1]:
            if open[-1] - low[-1] <= 0.005:
                if Spread(spread) == True:
                    settle_type = buy
                    price = mt5.symbol_info_tick(symbol).ask
                    magic = 555555
                    comment = "pat2_mom_buy"
                    req.normal_request(settle_type, price, magic, comment)
                    return True

def settlement(order_type):
    positions = mt5.positions_get(symbol=symbol, order_type)
    if positions:
        for position in positions:
            identifier = position[7]  # 保有ポジションの識別子
            price = position[13]  # 価格
            position_type = position[5]  # オーダータイプ
            magic = position[6]  # マジックナンバー
            comment = "range_settlement"

            if not position_type == order_type:  # 保有ポジションのタイプとこれからオーダーするポジションのタイプがダブらないようにする
                if position_type == buy and magic == 555555:
                    settle_type = sell  # 送信するオーダータイプ
                    req.settlement_request(settle_type, price, magic, comment, identifier)
                elif position_type == sell and magic == 555555:
                    settle_type = buy  # 送信するオーダータイプ
                    req.settlement_request(settle_type, price, magic, comment, identifier)



def range_price():
    mt5.initialize()
    dt_now = datetime.datetime.now()
    time_from = dt_now - datetime.timedelta(hours=9) # 3時間前の東京時間
    time_to = dt_now# - datetime.timedelta(hours=6) # 3時間前の東京時間
    # 2020.01.10 00:00-2020.01.11 13:00 UTCでUSDJPY M15からバーを取得する
 #   rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, time_from, time_to)
    rates = mt5.copy_rates_from_pos("USDJPY", mt5.TIMEFRAME_M15, 0, 10)
    df = pd.DataFrame(rates)

    df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')  # unix→標準
    df["time"] = df["time"] + pd.tseries.offsets.Hour(9)  # utc→9時間後

    #print(df)
#    print(df["close"])

    open = df["open"].tolist()
    close = df["close"].tolist()
    high = df["high"].tolist()
    low = df["low"].tolist()
    spread = df["spread"].tolist()

    flag = False

    if Sell(open, close, high, low, spread):
        settlement(Sell)
        print('Sell')
        flag = True
    if Buy(open, close, high, low, spread):
        settlement(Buy)
        print('Buy')
        flag = True
    if mom_Sell(open, close, high, low, spread):
        settlement(Sell)
        print('mom_Sell')
        flag = True
    if mom_Buy(open, close, high, low, spread):
        settlement(Buy)
        print('mom_Buy')
        flag = True

    if flag == False:
        print("レンジ帯：該当のパターン無し")


if __name__ == '__main__':
    settlement()
    range_price()





