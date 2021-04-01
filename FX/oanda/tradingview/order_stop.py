import MetaTrader5 as mt5
import param

account_ID = param.account_ID
password = param.password
symbol = param.symbol
threshold_profit = 200
settlement_profit = 30
deviation = param.deviation
lot = param.lot
magic = 1111111

identifers_list = []  # 利益がしきい値以上の時の識別子リスト
def order_up_down_settle():
    if mt5.initialize():
        authorized = mt5.login(account_ID, password=password)
        positions = mt5.positions_get(symbol=symbol)
    #    print("保有しているポジション数" ,len(positions))
        print("identifers_list:", identifers_list)
        for position in positions:  # 保有ポジションのうち利益がしきい値以上のものを識別子リストに追加
            profit = position[15]  # 利益
  #          profit = 200
            if threshold_profit <= profit:  # 利益がしきい値以上の時
                identifier = position[7]
                if not identifier in identifers_list: # 識別子が識別子リストに含まれていないとき
                    identifers_list.append(identifier)  # 識別子(identifier)を識別子リストに追加
    #            print(position)


        for position in positions:  # 保有ポジションの数だけ判定を行う
            identifier = position[7]  # 保有ポジションの識別子
            for identifer_list in identifers_list:  # 保有ポジションの識別子リストに識別子がある物の中から利益が決済しきい値以下のものを決済する
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
                        identifers_list.remove(identifier)  # 利益がしきい値以上の時の識別子リストから要素を取り出す
                        if result.retcode != mt5.TRADE_RETCODE_DONE:
                            message = "2. order_send failed, retcode={}".format(result.retcode)
                            print("order_send.py"+ message)


                            print("updownsettle",request)
    #                        print(result.comment)
                        #    Line_bot("order_send.py" + message)
        if not position: # 保有ポジションがないとき
            identifers_list = []  # 識別子リストを空にする

  #          print("identifers_list:",identifers_list)

              ##
if __name__ == '__main__':
    order_up_down_settle()