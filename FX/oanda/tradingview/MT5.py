import MetaTrader5 as mt5
from Line_bot import Line_bot

NARIYUKI_BUY = mt5.ORDER_TYPE_BUY  # 買い指値注文
NARIYUKI_SELL = mt5.ORDER_TYPE_SELL  # 売り指値注文

def order(order_type, sl_point, tp_point, lot):
    account_ID = 900006047
    password = "Hnm4264wtr"
    symbol = "GBPJPY"

    # MetaTrader 5に接続する
    # 接続完了→処理継続
    if mt5.initialize():
        print("接続確立完了。処理を継続します。")
        # パスワードとサーバを指定して取引口座に接続する
        authorized = mt5.login(account_ID, password=password)
        # GBPJPYのポジションを取得する
        positions = mt5.positions_get(symbol=symbol)

        # ポジションが2個以上→End
        if len(positions) >= 2:
            print("Total positions on" + symbol + "=", len(positions))
            Line_bot("ポジションを" + str(len(positions)) + "個保有中です。END")
            # すべてのポジションを表示する
            for position in positions:
                print(position)

        # ポジション無し→処理継続
        elif not positions :
            Line_bot("ポジションを" + str(len(positions)) + "個保有中です。処理継続")

            #lot = 0.1
            point = mt5.symbol_info(symbol).point  # 指定したシンボルの情報 point=最小の値動きの単位 ※値は0.001
            price = mt5.symbol_info_tick(symbol).ask  # 指定したシンボルの最後のtick時の情報 ask=買い注文の価格
            deviation = 20
            if order_type == NARIYUKI_BUY:
                sl = price - sl_point * point  # ※100*0.001=0.1
                tp = price + tp_point * point
            elif order_type == NARIYUKI_SELL:
                sl = price + sl_point * point
                tp = price - tp_point * point

            request = {
                "action": mt5.TRADE_ACTION_DEAL,         # 取引操作の種類。
                "symbol": symbol,                        # 注文が行われた取引商品の名前。注文を変更する場合と決済する場合は不要。
                "volume": lot,                           # ロット単位でのリクエストされた取引量。
                "type": order_type,                      # 注文の種類。
                "price": price,                          # 注文実行価格。
                "sl": sl,                                # 逆指値注文価格 ※100*0.001=0.1
                "tp": tp,                                # 指値注文価格
                "deviation": deviation,                  # リクエストされた価格からの最大許容偏差(ポイント単位)
                "magic": 234000,                         # EAのID。取引注文の分析処理を調整できるようにします。各EAは、取引リクエストを送信するときに一意のIDを設定できます。
                "comment": "python script open",         # 注文コメント。
                "type_time": mt5.ORDER_TIME_GTC,         # 注文有効期限の種類。値はORDER_TYPE_TIME値のうちの1つです。
                "type_filling": mt5.ORDER_FILLING_IOC,   # 注文の種類。値はORDER_TYPE_FILLING値のうちの1つです。
              #  "stoplimit": price + 0.1
            }
            # 取引リクエストを送信する
            result = mt5.order_send(request)
            # 実行結果を確認する
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
            print("逆指値:" , (price - 100 * point) , "\n指値" , (price + 100 * point))

            # リクエスト完了以外→End
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                message = "2. order_send failed, retcode={}".format(result.retcode)
                print(message)
                print(result.comment)
                Line_bot(message)

            # リクエスト完了
            else:
#                print("4. position #{} closed, {}".format(position_id, result))
                # 結果をディクショナリとしてリクエストし、要素ごとに表示する
                result_dict = result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field, result_dict[field]))
                    # これが取引リクエスト構造体の場合は要素ごとに表示する
#                    if field == "request":
#                        traderequest_dict = result_dict[field]._asdict()
#                    for tradereq_filed in traderequest_dict:
#                        print("traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
                print("リクエスト送信完了")
                Line_bot("リクエスト送信完了\n逆指値：" + str(sl) + "\n指値：" + str(tp))

    # 接続不可能→End
    else:
        message = "initialize() failed, error code =", mt5.last_error()
        print(message)
        Line_bot(message)

    # MetaTrader 5ターミナルへの接続をシャットダウンする
    mt5.shutdown()
    print('シャットダウン完了')

if __name__ == '__main__':
    print("実行開始")
    sl_point = 500
    tp_point = 100
    order(NARIYUKI_BUY, sl_point,tp_point, 0.1)