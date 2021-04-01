import MetaTrader5 as mt5
import sys
from Line_bot import Line_bot
from Line_bot import Line_bot_error
import backtest_variable
import time
import pandas as pd
import numpy as np
import datetime
import param

account_ID = param.account_ID
password = param.password
backtest = backtest_variable.backtest
positions_backtest= []
NARIYUKI_BUY = mt5.ORDER_TYPE_BUY  # 買い指値注文
NARIYUKI_SELL = mt5.ORDER_TYPE_SELL  # 売り指値注文
debug = False
profit_all = 0
carryover_position = 0
today = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
today = today + "バックテスト.csv"
backtest_log = "./バックテスト/" + today
#backtest_log = "./バックテスト/取引ログ.csv"
deviation = param.deviation

log_price = 0
log_tp = 0
log_sl = 0
act = False  # 決済処理を行うかフラグ　False→決済処理を行わない
if act == False:
    print("settlementpositionをおこないません")
elif act == True:
    print("settlementpositionをおこないます")
backtest_tp = 21
backtest_sl = 10
if backtest == True:  # バックテスト
    positions = []

# オーダー送信関数
def order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid, df):
    if backtest == False: # 本番
        point = mt5.symbol_info(symbol).point  # 指定したシンボルの情報 point=最小の値動きの単位 ※値は0.001
        spread = price_ask - price_bid
    elif backtest == True:  # バックテスト
        point = 0.001
        spread = price_ask - price_bid
        spread = spread.tolist()
#        spread = spread[0]

    deviation = 20
    permit_spread = 0.004
    #spread = price_ask - price_bid

    # スプレッドが基準以下の時　→　処理継続
    if spread <= permit_spread:

        # 買い注文時の価格
        if order_type == NARIYUKI_BUY:
            price = price_ask
            if backtest == True:
                price_settle = price_bid  # 決済は逆のポジションを基準に考える
                sl = price_settle - sl_point * point  # ※100*0.001=0.1
                tp = price_settle + tp_point * point
            elif backtest == False:
                sl = price - sl_point * point  # ※100*0.001=0.1
                tp = price + tp_point * point
        # 売り注文時の価格
        elif order_type == NARIYUKI_SELL:
            price = price_bid
            if backtest == True:
                price_settle = price_ask    # 決済は逆のポジションを基準に考える
                sl = price_settle + sl_point * point
                tp = price_settle - tp_point * point
            elif backtest == False:
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
            "magic": magic,                          # EAのID。取引注文の分析処理を調整できるようにします。各EAは、取引リクエストを送信するときに一意のIDを設定できます。
            "comment": "python script open",         # 注文コメント。
            "type_time": mt5.ORDER_TIME_GTC,         # 注文有効期限の種類。値はORDER_TYPE_TIME値のうちの1つです。
            "type_filling": mt5.ORDER_FILLING_IOC,   # 注文の種類。値はORDER_TYPE_FILLING値のうちの1つです。
          #  "stoplimit": price + 0.1
        }

        if backtest == False:  # 本番
            # 取引リクエストを送信する
            result = mt5.order_send(request)
            # 実行結果を確認する
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
        #    print("逆指値:" , (price - 100 * point) , "\n指値" , (price + 100 * point))
            print("request",request)
            # リクエスト完了以外→End
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                message = "2. order_send failed, retcode={}".format(result.retcode)
                print(message)
                print(result.comment)
                Line_bot_error(message)

            # リクエスト完了
            else:
#                 print("4. position #{} closed, {}".format(position_id, result))
                 # 結果をディクショナリとしてリクエストし、要素ごとに表示する
                result_dict = result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field, result_dict[field]))
                    # これが取引リクエスト構造体の場合は要素ごとに表示する
#                     if field == "request":
#                         traderequest_dict = result_dict[field]._asdict()
#                     for tradereq_filed in traderequest_dict:
#                         print("traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
                print("リクエスト送信完了")
                Line_bot("リクエスト送信完了\n価格：" + str(price) + "逆指値：" + str(sl) + "\n指値：" + str(tp))

        elif backtest == True:  # バックテスト
            global positions_backtest
            high = df.iat[-2, 2] # 予測した時間の実際の価格(high)
            low = df.iat[-2, 3] # 予測した時間の実際の価格(low)
            time = df.iat[-2, 0]  # 予測した時間(予測後ではない)
            time = time + datetime.timedelta(hours=9)  # 日本時間を計算
            time = "{0:%Y-%m-%d %H:%M}".format(time)
            lot = 10000
            profit = 0
            global profit_all
            global carryover_position

            with open(backtest_log, mode="a",encoding="shift_jis") as f:
                # 買い注文→売り決済時の判定
                if order_type == NARIYUKI_BUY:  # 値は0
                    if sl > low:  # slが成立
                        profit = (sl - price_bid) * lot
                        print('sl買い注文売り決済成立:', profit)
                        profit_all += profit
                    elif tp < high:  # tpが成立
                        profit = (tp - price_bid) * lot
                        print('tp買い注文売り決済成立:', profit)
                        profit_all += profit
                    else:  # ポジション持ち越し
                        carryover_position += 1
                        positions_backtest.append([0,0,0,0,0,order_type,0,0,0,lot,0,sl,tp,0,0,0,symbol,price_ask,price_bid])
                        tp = 'ポジション持ち越し'
                        sl = 'ポジション持ち越し'
                # 売り注文→買い決済時の判定
                elif order_type == NARIYUKI_SELL:  # 値は1
                    if sl < high:  # slが成立
                        profit = (price_ask - sl) * lot
                        print('sl売り注文買い決済成立:', profit)
                        profit_all += profit
                    elif tp > low:  # tpが成立
                        profit = (price_ask - tp) * lot
                        print('tp売り注文買い決済成立:', profit)
                        profit_all += profit
#必要なし0327                        del positions_backtest[]
                    else:  # ポジション持ち越し
                        carryover_position += 1
                        positions_backtest.append([0,0,0,0,0,order_type,0,0,0,lot,0,sl,tp,0,0,0,symbol,price_ask,price_bid])
                        tp = 'motikosi'

                    if sl_point == 0:
                        tp = "予測値が同じためオーダーしない"
                        sl = "予測値が同じためオーダーしない"
                f.write(str(time) + "," + str(profit) + "," + str(order_type) + "," + str(tp) + "," + str(sl)\
                        + "," + str(price_ask) + "," + str(price_bid) + "," + str(high) + "," + str(low) + "," + str(profit_all)+ "\n")
        print('profit_all:', profit_all)
        global log_price
        global log_tp
        global log_sl
        log_price = price
        log_tp = tp
        log_sl = sl

#            print(high)
        #time.sleep(10)
    else:
        print("分岐3:スプレッドが広いため処理を終了します")
        Line_bot("分岐3:スプレッドが広いため処理を終了します")

# 保有ポジションがプラス収支の場合に決済する関数
# 保有ポジションがマイナスの時はtpを0.005変更する
def settlement_position(position, MACD_judge, price_ask, price_bid):
    profit = position[15]  # 現在の利益
    position_id = position[7]  # ポジションID
    price_current = position[13]  # 現在の価格
    magic = position[6]  # magicナンバー
    symbol = position[16]
    lot = position[9]
    price_open = position[10]
    sl = position[11]
    tp = position[12]
    order_type = position[5]
    settle_flag = False

    #　損切り処理
#    if order_type == NARIYUKI_SELL:   # 注文が売りの時は
    if MACD_judge == NARIYUKI_SELL and order_type == NARIYUKI_BUY:  # MACDが売りシグナルの時は買いポジションを手放す
        type = NARIYUKI_SELL           # 決済が買い
        change_tp = price_open - 0.005
        settle_flag = True
#    elif order_type == NARIYUKI_BUY:  # 注文が買いの時は
    elif MACD_judge == NARIYUKI_BUY and order_type == NARIYUKI_SELL:
        type = NARIYUKI_BUY          # 決済が売り
        change_tp = price_open + 0.005
        settle_flag = True



#    if 0 < profit:
    print("settle_flag:",settle_flag)
    if settle_flag == True:  # MACDのシグナルに保有ポジションが該当している(トレンドが変わったら現在価格で損切りする)
        if backtest == False :  # 本番

            global act  # `決済処理を行うかフラグ False→決済処理を行わない
            if act == False:  # 決済処理を行わない
                return True
            # 決済リクエストを作成する
           # position_id = result.order
           # price = mt5.symbol_info_tick(symbol).bid
            elif act == True:         # 決済処理を行う
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": type,
                    "position": position_id,
                    "price": price_current,
                    "deviation": deviation,
                    "magic": magic,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                result = mt5.order_send(request)

                # リクエスト完了以外→End
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    message = "2. order_send failed, retcode={}".format(result.retcode)
                    print(message)
                    print(result.comment)
                    Line_bot(message)
                    return False
                # リクエスト完了
                else:
                    # 結果をディクショナリとしてリクエストし、要素ごとに表示する
                    result_dict = result._asdict()
                    for field in result_dict.keys():
                        print("   {}={}".format(field, result_dict[field]))
                    #print("リクエスト送信完了")
                    Line_bot("settle_flag:" + str(settle_flag) + "決済リクエスト送信完了\n利益：" + str(profit)
                             + "\nオープン価格：" + str(price_open)+ "\n現在価格：" + str(price_current))
                    return True  #

        if backtest == True :  # バックテスト
            global profit_all
            global carryover_position
            global backtest_sl
            when_price_ask = position[17]  # 注文時の価格
            when_price_bid = position[18]  # 注文時の価格

            if order_type == NARIYUKI_BUY:  # 買い注文→売り決済
                profit = (when_price_ask - price_bid) * lot
                profit = backtest_sl * -10 # 暫定処理03.14
                print('settlement:', profit)
                profit_all += profit

            # 売り注文→買い決済時の判定
            elif order_type == NARIYUKI_SELL:  # 売り注文→買い決済
                profit = (when_price_bid - price_ask) * lot
                profit = backtest_sl * -10  # 暫定処理03.14
                print('settlement:', profit)
                profit_all += profit
            with open(backtest_log, mode="a", encoding="utf-8") as f:
                f.write("settlement," + str(profit) + "\n")

            return True


#       elif settle_flag == False:  # MACDのシグナルに保有ポジションが該当している
#           request = {
#               "action": mt5.TRADE_ACTION_SLTP,
#               "symbol": symbol,
#               "volume": lot,
#                "type": type,
#               "position": position_id,
#                "price": price,
#               "deviation": deviation,
#               "magic": magic,
#               "tp": change_tp,
#               "sl":sl,
#               "comment": "python script close",
#               "type_time": mt5.ORDER_TIME_GTC,
#               "type_filling": mt5.ORDER_FILLING_IOC,
#           }
#
        result = mt5.order_send(request)
        print(request)
    #    print('保有ポジションの評価がマイナスのため決済を行いません')
    #    Line_bot('保有ポジションの評価がマイナスのため決済を行いません')
        return False

# オーダー判定関数
def order(order_type, sl_point, tp_point, lot, magic, symbol, MACD_judge, Cross_judge,df,order_flag=True):
#    account_ID = 900006047
#    password = "Hnm4264wtr"
    #order_flag = True
    max_positions = 1  # 指定した数値が保有できる最大ポジション数になる
    global positions
    # MetaTrader 5に接続する
    # 接続完了→処理継続

    if backtest == False:  # 本番
        if mt5.initialize():
            print("接続確立完了。処理を継続します。")
            # パスワードとサーバを指定して取引口座に接続する
            authorized = mt5.login(account_ID, password=password)
            # GBPJPYのポジションを取得する
            positions = mt5.positions_get(symbol=symbol)
            price_ask = mt5.symbol_info_tick(symbol).ask  # 指定したシンボルの最後のtick時の情報 ask=買い注文の価格
            price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 bid=売り注文の価格
       #     print(positions)
    elif backtest == True:  # バックテスト
        price_ask = df.iat[-2,1]  # 最終行から2つ目(現在)のopen価格
        price_bid = price_ask -0.003

    # 保有ポジションがある場合 → 保有ポジションの決済処理 & 保有ポジションのmagicナンバーを取り出してリストに格納
    if positions :
        magic_nums = []  # magicナンバーのリスト
        position_types = []  # 保有ポジションタイプのリスト
        i = 0
        for position in positions:
            resultsettlement_position = settlement_position(position, MACD_judge,price_ask,price_bid)  # 保有ポジションがプラス収支の場合に決済する関数
            if resultsettlement_position == False:  # 保有ポジションの決済を行っていないとき　→　ポジションを保有しているので
                magic_nums.append(position[6])  # 全ての保有ポジションmagicナンバーを取り出してリストに追加
                if order_type == position[5]:  # これからオーダーしようとしているのオーダータイプと保有ポジションのオーダータイプが同じとき
                    position_types.append(position[5])  # ポジションタイプを追加(所持しているポジション数を把握したい)
            if resultsettlement_position == True and backtest == True:  # バックテストかつポジションの決済が完了したとき
                del positions_backtest[i]  # 対象のポジションのリストを削除
            i += 1
        position_types_count = len(position_types)
    # 保有ポジションがない場合 → 保有ポジション数 = 0
    else:
        position_types_count = 0

    print("positions", positions)

  #使わない  if order_flag == False:
  #使わない      print("order_flag:False")

    # ポジション無し→オーダー送信
    if 0 == position_types_count :
        print("分岐1:同ポジションを" + str(position_types_count) + "個保有中です。処理継続")
    #    Line_bot("分岐1:ポジションを" + str(len(positions)) + "個保有中です。処理継続")
        order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid, df)  # オーダー送信


    # 同ポジションタイプがmax_positions個以上→End
    elif max_positions <= position_types_count:
        print("分岐1:同ポジションを" + str(position_types_count) + "個持っているため処理を終了します")
        if backtest == False:  # 本番
            Line_bot("分岐1:同ポジションを" + str(position_types_count) + "個持っているため処理を終了します")
        elif backtest == True:  # バックテスト
            time = df.iat[-1, 0]  # 予測した時間(予測後ではない)
            time = time + datetime.timedelta(hours=9)  # 日本時間を計算
            time = "{0:%Y-%m-%d %H:%M}".format(time)

            with open(backtest_log, mode="a", encoding="shift_jis")as f:
                f.write(str(time) + ",ポジションを上限まで保有中\n")

    # ポジション数が1以上、max_positions未満→magicナンバー判定を行う
    # ※ magicナンバーが一致 → オーダーしない
    # ※ magicナンバーが一致 → オーダーする

    # 保有ポジションが1以上、max_positions(閾値)以下の場合
    elif 1 <= position_types_count <= max_positions:
        # 保有ポジションとオーダーポジションのmagicナンバーを判定
        for magic_num in magic_nums:
            # 全ての保有ポジションとオーダーポジションのmagicナンバーが違う→処理継続
            if magic_num != magic:
                print("処理継続")
            # 1つでも保有ポジションとオーダーポジションのmagicナンバーが同じ→End
            elif magic_nums == magic:
                print("既に持っている同ポジションです。End")
                order_flag = False

        # オーダーフラグがTrue→オーダー送信
        if order_flag == True:
            print("分岐2:同じmagicナンバーのポジションが無いため処理継続します")
        #    Line_bot("分岐2:同じmagicナンバーのポジションが無いため処理継続します")
            order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid, df)  # オーダー送信

        # オーダーフラグがFalse→オーダーしない
        elif order_flag == False:
            print("分岐2:既に同じmagicナンバーのポジションを保有しています:" + magic)
            Line_bot("分岐2:既に同じmagicナンバーのポジションを保有しています:" + magic)

    # 接続不可能→End
    #else:
    #    message = "initialize() failed, error code =", mt5.last_error()
    #    print(message)
    #    Line_bot(message)

    # MetaTrader 5ターミナルへの接続をシャットダウンする
    mt5.shutdown()
    #print('シャットダウン完了')

if __name__ == '__main__':
    debug = True
    print("実行開始")
    sl_point = 500
    tp_point = 100
    magic = 234000
    symbol = 'USDJPY'
    MACD_judge = 9
    Cross_judge = 9
    lot = 0.01
    order(order, sl_point,tp_point, lot, magic, symbol, MACD_judge, Cross_judge)