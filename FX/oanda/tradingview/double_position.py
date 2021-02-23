import MetaTrader5 as mt5
import time

symbol = "GBPJPY"
lot = 0.1
deviation = 0
permit_spread = 0.01
account_ID = 900006047
password = "Hnm4264wtr"
NARIYUKI_BUY = mt5.ORDER_TYPE_BUY  # 買い指値注文
NARIYUKI_SELL = mt5.ORDER_TYPE_SELL  # 売り指値注文

def request(symbol, lot, order_type, price,sl, tp, magic):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # 取引操作の種類。
        "symbol": symbol,  # 注文が行われた取引商品の名前。注文を変更する場合と決済する場合は不要。
        "volume": lot,  # ロット単位でのリクエストされた取引量。
        "type": order_type,  # 注文の種類。
        "price": price,  # 注文実行価格。
        "sl": sl,  # 逆指値注文価格 ※100*0.001=0.1
        "tp": tp,  # 指値注文価格
        "deviation": deviation,  # リクエストされた価格からの最大許容偏差(ポイント単位)
        "magic": magic,  # EAのID。取引注文の分析処理を調整できるようにします。各EAは、取引リクエストを送信するときに一意のIDを設定できます。
        "comment": "python script open",  # 注文コメント。
        "type_time": mt5.ORDER_TIME_GTC,  # 注文有効期限の種類。値はORDER_TYPE_TIME値のうちの1つです。
        "type_filling": mt5.ORDER_FILLING_IOC,  # 注文の種類。値はORDER_TYPE_FILLING値のうちの1つです。
        #  "stoplimit": price + 0.1
    }
    # 取引リクエストを送信する
    result = mt5.order_send(request)

    # リクエスト完了以外→End
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        message = "2. order_send failed, retcode={}".format(result.retcode)
        print(message)
        print(result.comment)
    #    Line_bot(message)

    # リクエスト完了
    else:
        # 結果をディクショナリとしてリクエストし、要素ごとに表示する
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
        print("リクエスト送信完了")
    #    Line_bot("リクエスト送信完了\n逆指値：" + str(sl) + "\n指値：" + str(tp))


def order_send(order_type, sl_point, tp_point, lot, magic, symbol):
    point = mt5.symbol_info(symbol).point  # 指定したシンボルの情報 point=最小の値動きの単位 ※値は0.001
    price_ask = mt5.symbol_info_tick(symbol).ask  # 指定したシンボルの最後のtick時の情報 ask=買い注文の価格
    price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 bid=売り注文の価格

    positions = mt5.positions_get(symbol=symbol)
    if 1 <= len(positions):  # ポジションを保有しているとき

        spread = price_ask - price_bid
        # スプレッドが基準以下の時　→　処理継続
        if spread <= permit_spread:
            # 買い注文時の価格
            price = price_ask
            sl = price - 100 * point  # ※100*0.001=0.1
            tp = price + 1000 * point
            magic = 200000
            request = request(symbol, lot, NARIYUKI_BUY, price, sl, tp, magic)  # 買い注文

            # 売り注文時の価格
            price = price_bid
            sl = price + 100 * point
            tp = price - 1000 * point
            magic = 200001
            request = request(symbol, lot, NARIYUKI_SELL, price, sl, tp, magic)  # 売り注文
            # スプレッドが広い時
        elif spread > permit_spread:
            print('スプレッドが広い')

    elif not positions:
        print("ポジションを保有していません")

    # MetaTrader 5に接続する
    # 接続完了→処理継続
if mt5.initialize():
    print("接続確立完了。処理を継続します。")
    # パスワードとサーバを指定して取引口座に接続する
    authorized = mt5.login(account_ID, password=password)

while True:
    order_send(order_type, sl_point, tp_point, lot, magic, symbol)
    time.sleep(10)