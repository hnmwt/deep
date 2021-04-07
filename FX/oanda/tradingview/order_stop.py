import MetaTrader5 as mt5
import param

account_ID = param.account_ID
password = param.password
symbol = param.symbol
threshold_profit = 200
settlement_profit = 40
deviation = param.deviation
lot = param.lot
magic = 1111111

up_down_identifers_list = []  # 利益がしきい値以上の時の識別子リスト
min1_price_bid = 0
rapid_change_identifiers = []
def order_up_down_settle(positions):
    if positions:
        global up_down_identifers_list

    # 21.04.07廃止   positions = mt5.positions_get(symbol=symbol)
    #    print("保有しているポジション数" ,len(positions))
   #     print("up_down_identifers_list:", up_down_identifers_list)
        for position in positions:  # 保有ポジションのうち利益がしきい値以上のものを識別子リストに追加
            profit = position[15]  # 利益
  #          profit = 200
            if threshold_profit <= profit:  # 利益がしきい値以上の時
                identifier = position[7] # 識別子
                if not identifier in up_down_identifers_list: # 識別子が識別子リストに含まれていないとき
                    up_down_identifers_list.append(identifier)  # 識別子(identifier)を識別子リストに追加
    #            print(position)


        for position in positions:  # 保有ポジションの数だけ判定を行う
            identifier = position[7]  # 保有ポジションの識別子
            for identifer_list in up_down_identifers_list:  # 保有ポジションの識別子リストに識別子がある物の中から利益が決済しきい値以下のものを決済する
                if identifier == identifer_list: # 保有ポジションの識別子としきい値以上の時の識別子が一致したとき == 決済確認対象になる
                    profit = position[15]  # 利益
 #                   profit = 40
                    if 0 < profit <= settlement_profit: # 利益が決済しきい値を下回るとき即決済する

                        position_type = position[5]
                        if position_type == 0:
                            settle_type = 1  # 送信するオーダータイプ
                        elif position_type == 1:
                            settle_type = 0  # 送信するオーダータイプ

                        request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": symbol,
                            "volume": lot,
                            "type": settle_type,
                            "position": identifier,
                            "price": position[13],  # 現在の価格,
                            "deviation": deviation,
                            "magic": magic,
                            "comment": "python up down settle",
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_IOC,
                        }
                        result = mt5.order_send(request)
                        up_down_identifers_list.remove(identifier)  # 利益がしきい値以上の時の識別子リストから要素を取り出す
                        if result.retcode != mt5.TRADE_RETCODE_DONE:
                            message = "2. order_send failed, retcode={}".format(result.retcode)
                            print("order_send.py"+ message)


                            print("updownsettle",request)
    #                        print(result.comment)
                        #    Line_bot("order_send.py" + message)
    if not positions: # 保有ポジションがないとき
        up_down_identifers_list = []  # 識別子リストを空にする

  #          print("up_down_identifers_list:",up_down_identifers_list)

def rapid_change(positions):
    if positions:
        price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 ※askは朝方スプレッドが広がるためbidにする
        if abs(price_bid - min1_price_bid) > 0.018:  # 価格が指定した値以上変化していた場合
            global rapid_change_identifiers
            for position in positions:  # 保有ポジション分処理を回す
                profit = position[15]  # 利益
                if profit < 0: # 利益が0以下の場合
                    identifier = position[7]  # 識別子
                    if not identifier in rapid_change_identifiers: # 識別子が配列の中にない場合(処理をまだ行っていない)
                        rapid_change_identifiers.append(identifier) # 識別子を追加

                        position_type = position[5]  # 対象のポジションのオーダータイプ
                        if position_type == 0:
                            settle_type = 1  # 送信するオーダータイプ
                            price = price_bid
                        elif position_type == 1:
                            settle_type = 0  # 送信するオーダータイプ
                            price = mt5.symbol_info_tick(symbol).ask
                        sl = position[12]  # 対象のポジションのtpを新しくオーダーするslにする
                        tp = position[11]  # 対象のポジションのslを新しくオーダーするtpにする
                        magic = 222222
                        comment = "rapid_change"
                        message = request(settle_type=settle_type, identifier=identifier, price=price, sl=sl, tp=tp, magic=magic, comment=comment)
                        print(message)
    if not positions:  # 保有ポジションがないとき
        rapid_change_identifiers = []  # 識別子リストを空にする
                    


def request(settle_type, identifier, price, sl, tp, magic, comment):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": settle_type,
        "position": identifier,
        "price": price,  # 現在の価格,
        "sl": sl,  # 逆指値注文価格 ※100*0.001=0.1
        "tp": tp,  # 指値注文価格
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        message = "2. order_send failed, retcode={}".format(result.retcode)
    return message

if __name__ == '__main__':
    order_up_down_settle()