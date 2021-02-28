import MetaTrader5 as mt5
import sys
from Line_bot import Line_bot

NARIYUKI_BUY = mt5.ORDER_TYPE_BUY  # 買い指値注文
NARIYUKI_SELL = mt5.ORDER_TYPE_SELL  # 売り指値注文
debug = False
# オーダー送信関数
def order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid):
    point = mt5.symbol_info(symbol).point  # 指定したシンボルの情報 point=最小の値動きの単位 ※値は0.001
    deviation = 20
    permit_spread = 0.011
    spread = price_ask - price_bid

    # スプレッドが基準以下の時　→　処理継続
    if spread <= permit_spread:
    # 買い注文時の価格
        if order_type == NARIYUKI_BUY:
            price = price_ask
            sl = price - sl_point * point  # ※100*0.001=0.1
            tp = price + tp_point * point
        # 売り注文時の価格
        elif order_type == NARIYUKI_SELL:
            price = price_bid
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
#             print("4. position #{} closed, {}".format(position_id, result))
             # 結果をディクショナリとしてリクエストし、要素ごとに表示する
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # これが取引リクエスト構造体の場合は要素ごとに表示する
#                 if field == "request":
#                     traderequest_dict = result_dict[field]._asdict()
#                 for tradereq_filed in traderequest_dict:
#                     print("traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            print("リクエスト送信完了")
            Line_bot("リクエスト送信完了\n逆指値：" + str(sl) + "\n指値：" + str(tp))

    else:
        print("分岐3:スプレッドが広いため処理を終了します")
        Line_bot("分岐3:スプレッドが広いため処理を終了します")

# 保有ポジションがプラス収支の場合に決済する関数
# 保有ポジションがマイナスの時はtpを0.005変更する
def settlement_position(position):
    profit = position[15]  # 現在の利益
    position_id = position[7]  # ポジションID
    price = position[13]  # 現在の価格
    magic = position[6]  # magicナンバー
    symbol = position[16]
    lot = position[9]
    price_open = position[10]
    sl = position[11]
    tp = position[12]
    if position[5] == 1:
        type = NARIYUKI_BUY
        change_tp = price_open - 0.005
    elif position[5] == 0:
        type = NARIYUKI_SELL
        change_tp = price_open + 0.005

    deviation = 20
    # 利益がプラスの時
    if 0 < profit:
        # 決済リクエストを作成する
       # position_id = result.order
       # price = mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": type,
            "position": position_id,
            "price": price,
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
            Line_bot("決済リクエスト送信完了\n利益：" + str(profit))
            return True  #

    # 利益がマイナスの時
    elif 0 >= profit:
#        request = {
#            "action": mt5.TRADE_ACTION_SLTP,
#            "symbol": symbol,
#            "volume": lot,
#            "type": type,
#            "position": position_id,
#            "price": price,
#            "deviation": deviation,
#            "magic": magic,
#            "tp": change_tp,
#            "sl":sl,
#            "comment": "python script close",
#            "type_time": mt5.ORDER_TIME_GTC,
#            "type_filling": mt5.ORDER_FILLING_IOC,
#        }
#
#        result = mt5.order_send(request)
#        print(request)
#    #    print('保有ポジションの評価がマイナスのため決済を行いません')
#    #    Line_bot('保有ポジションの評価がマイナスのため決済を行いません')
        return False

# オーダー関数
def order(order_type, sl_point, tp_point, lot, magic, symbol):
    account_ID = 900006047
    password = "Hnm4264wtr"
    order_flag = True
    max_positions = 2  # 指定した数値が保有できる最大ポジション数になる

    # MetaTrader 5に接続する
    # 接続完了→処理継続
    if mt5.initialize():
        print("接続確立完了。処理を継続します。")
        # パスワードとサーバを指定して取引口座に接続する
        authorized = mt5.login(account_ID, password=password)
        # GBPJPYのポジションを取得する
        positions = mt5.positions_get(symbol=symbol)
        price_ask = mt5.symbol_info_tick(symbol).ask  # 指定したシンボルの最後のtick時の情報 ask=買い注文の価格
        price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 bid=売り注文の価格

        # 保有ポジションがある場合 → 保有ポジションの決済処理 & 保有ポジションのmagicナンバーを取り出してリストに格納
        if positions :
            magic_nums = []  # magicナンバーのリスト
            position_types = []  # 保有ポジションタイプのリスト
            for position in positions:
                resultsettlement_position = settlement_position(position)  # 保有ポジションがプラス収支の場合に決済する関数
                if resultsettlement_position == False:  # 保有ポジションの決済を行っていないとき　→　ポジションを保有しているので
                    magic_nums.append(position[6])  # 全ての保有ポジションmagicナンバーを取り出してリストに追加
                    if order_type == position[5]:  # オーダータイプと保有ポジションのタイプが同じとき
                        position_types.append(position[5])  # ポジションタイプを追加
            position_types_count = len(position_types)

        # 保有ポジションがない場合 → 保有ポジション数 = 0
        else:
            position_types_count = 0

        if debug == True:
            print("debugのためブレイク")
            sys.exit()
        # ポジション無し→オーダー送信
        if 0 == position_types_count :
            print("分岐1:同ポジションを" + str(position_types_count) + "個保有中です。処理継続")
        #    Line_bot("分岐1:ポジションを" + str(len(positions)) + "個保有中です。処理継続")
            order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid)  # オーダー送信

        # 同ポジションタイプがmax_positions個以上→End
        elif max_positions <= position_types_count:
            print("分岐1:同ポジションを" + str(position_types_count) + "個持っているため処理を終了します")
            Line_bot("分岐1:同ポジションを" + str(position_types_count) + "個持っているため処理を終了します")

        # ポジション数が1以上、max_positions未満→magicナンバー判定を行う
        # ※ magicナンバーが一致 → オーダーしない
        # ※ magicナンバーが一致 → オーダーする

        # 保有ポジションが1以上、max_positions未満の場合
        elif 1 <= position_types_count < max_positions:
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
                order_send(order_type, sl_point, tp_point, lot, magic, symbol, price_ask, price_bid)  # オーダー送信

            # オーダーフラグがFalse→オーダーしない
            elif order_flag == False:
                print("分岐2:既に同じmagicナンバーのポジションを保有しています:" + magic)
                Line_bot("分岐2:既に同じmagicナンバーのポジションを保有しています:" + magic)

    # 接続不可能→End
    else:
        message = "initialize() failed, error code =", mt5.last_error()
        print(message)
        Line_bot(message)

    # MetaTrader 5ターミナルへの接続をシャットダウンする
    mt5.shutdown()
    print('シャットダウン完了')

if __name__ == '__main__':
    debug = True
    print("実行開始")
    sl_point = 500
    tp_point = 100
    magic = 234000
    symbol = 'GBPJPY'
    order(NARIYUKI_BUY, sl_point,tp_point, 0.1, magic, symbol)