import MetaTrader5 as mt5

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

    # ポジション保有中→End
    if len(positions) > 0:
        print("Total positions on" + symbol + "=", len(positions))
        # すべてのポジションを表示する
        for position in positions:
            print(position)

    # ポジション無し→処理継続
    elif not positions :
        print("ポジションを保有していません。処理を継続します。")

        lot = 0.1
        point = mt5.symbol_info(symbol).point  # 指定したシンボルの情報 point=最小の値動きの単位
        price = mt5.symbol_info_tick(symbol).ask  # 指定したシンボルの最後のtick時の情報 ask=買い注文の価格
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,         # 取引操作の種類。
            "symbol": symbol,                        # 注文が行われた取引商品の名前。注文を変更する場合と決済する場合は不要。
            "volume": lot,                           # ロット単位でのリクエストされた取引量。
            "type": mt5.ORDER_TYPE_BUY,              # 注文の種類。
            "price": price,                          # 注文実行価格。
            "sl": price - 100 * point,               # 逆指値注文価格
            "tp": price + 100 * point,               # 指値注文価格
            "deviation": deviation,                  # リクエストされた価格からの最大許容偏差(ポイント単位)
            "magic": 234000,                         # EAのID。取引注文の分析処理を調整できるようにします。各EAは、取引リクエストを送信するときに一意のIDを設定できます。
            "comment": "python script open",         # 注文コメント。
            "type_time": mt5.ORDER_TIME_GTC,         # 注文有効期限の種類。値はORDER_TYPE_TIME値のうちの1つです。
            "type_filling": mt5.ORDER_FILLING_RETURN,# 注文の種類。値はORDER_TYPE_FILLING値のうちの1つです。
        }
        # 取引リクエストを送信する
        result = mt5.order_send(request)
        # 実行結果を確認する
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))

        else:
            print("4. position #{} closed, {}".format(position_id, result))
            # 結果をディクショナリとしてリクエストし、要素ごとに表示する
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # これが取引リクエスト構造体の場合は要素ごとに表示する
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

# 接続不可能→End
else:
    print("initialize() failed, error code =", mt5.last_error())

# MetaTrader 5ターミナルへの接続をシャットダウンする
mt5.shutdown()
print('シャットダウン完了')