import MetaTrader5 as mt5
import param

account_ID = param.account_ID
password = param.password
symbol = param.symbol
threshold_profit = 200
settlement_profit = 120
rapid_change_threshold = 0.008
deviation = param.deviation
lot = param.lot


up_down_identifers_list = []  # 利益がしきい値以上の時の識別子リスト
min1_price_bid = 0
rapid_change_identifiers = []

#  ***** def order_up_down_settle(positions)の役割 *******
#  1.ポジションが「上がる→下がる」とき決済する
#  2.rapid_changeで注文したポジションがプラスの時決済する
#
def order_up_down_settle(positions):
    if positions:
        mt5.initialize()
        global up_down_identifers_list

    # 21.04.07廃止   positions = mt5.positions_get(symbol=symbol)
    #    print("保有しているポジション数" ,len(positions))
   #     print("up_down_identifers_list:", up_down_identifers_list)
        for position in positions:  # 保有ポジションのうち利益がしきい値以上のものを識別子リストに追加
            profit = position[15]  # 利益
  #          profit = 140
            if threshold_profit <= profit:  # 利益がしきい値以上の時
                identifier = position[7] # 識別子
                if not identifier in up_down_identifers_list: # 識別子が識別子リストに含まれていないとき
                    up_down_identifers_list.append(identifier)  # 識別子(identifier)を識別子リストに追加
                    print('up_down_identifers_list', up_down_identifers_list)
    #            print(position)


        for position in positions:  # 保有ポジションの数だけ判定を行う
            identifier = position[7]  # 保有ポジションの識別子
            profit = position[15]  # 利益
            price = position[13] # 価格
            position_type = position[5] # オーダータイプ
            magicNo = position[6] # マジックナンバー
            for identifer_list in up_down_identifers_list:  # 保有ポジションの識別子リストに識別子がある物の中から利益が決済しきい値以下のものを決済する
                if identifier == identifer_list: # 保有ポジションの識別子としきい値以上の時の識別子が一致したとき == 決済確認対象になる
 #                   profit = 50
                    if 0 < profit <= settlement_profit:  # 利益が決済しきい値を下回るとき即決済する
                        if position_type == 0:
                            settle_type = 1  # 送信するオーダータイプ
                        elif position_type == 1:
                            settle_type = 0  # 送信するオーダータイプ
                        comment = "python up down settle"
                        magic = 111111

                        message = prompt_request(settle_type, price, magic, comment, identifier)  # 即決済する

            if magicNo == 222222 or 222221 or 234000 or 235000:  # rapid_changeの注文識別子の時
                if 40 < profit :  # 利益が40以上
                    if position_type == 0:
                        settle_type = 1  # 送信するオーダータイプ
                    elif position_type == 1:
                        settle_type = 0  # 送信するオーダータイプ
                    comment = "rapid_change_settle"
                    magic = 333333
                    message = prompt_request(settle_type, price, magic, comment, identifier)  # 即決済する



    if not positions: # 保有ポジションがないとき
        up_down_identifers_list = []  # 識別子リストを空にする

  #          print("up_down_identifers_list:",up_down_identifers_list)

#  ***** def rapid_change(positions)の役割 *******
#  1.ポジションが一定以上変化&マイナス評価の時逆の注文をする
#  2.rapid_changeで注文したポジションがプラスの時決済する
#
def rapid_change(positions):
    mt5.initialize()
    price_bid = mt5.symbol_info_tick(symbol).bid  # 指定したシンボルの最後のtick時の情報 ※askは朝方スプレッドが広がるためbidにする
    global min1_price_bid
    if positions:
        if abs(price_bid - min1_price_bid) > rapid_change_threshold:  # 価格が指定した値以上変化していた場合
            global rapid_change_identifiers
            magicNo_flag_222222 = False
            magicNo_flag_222221 = False

            for position in positions:
                if position[6] == 222222:  # マジックナンバーが222221,222222のリストが１つでもあったときは無駄なリクエストを送信しないようにする
                    magicNo_flag_222222 = True  # 222222所持フラグをtrueにする
                if position[6] == 222221:  # マジックナンバーが222221,222222のリストが１つでもあったときは無駄なリクエストを送信しないようにする
                    magicNo_flag_222221 = True  # 222221所持フラグをtrueにする

            #***************************
            # 222222(売り)を持っていないときの処理
            #***************************
            if magicNo_flag_222222 == False:   # 222222所持フラグがFalseの時に処理をする
                settlementFlag = False
                for position in positions:  # 保有ポジション分処理を回す
                    profit = position[15]  # 利益
                    magicNo = position[6]  # マジックナンバー
                    if profit < 0 and magicNo != 222222:  # 利益が-100以下の場合かつ保有ポジションのマジックナンバーが222222以外の時
                        identifier = position[7]  # 識別子
                        if not identifier in rapid_change_identifiers:  # 識別子が配列の中にない場合(処理をまだ行っていない)
                        #    rapid_change_identifiers.append(identifier) # 識別子を配列に追加。識別子が配列にある間は下記の処理を行わない

                            position_type = position[5]  # 対象のポジションのオーダータイプ
                            if position_type == 0:
                                if settlementFlag == False:
                                    settle_type = 1  # 送信するオーダータイプ(売り)
                                    price = price_bid
                                 #   sl = position[12] + 0.003  # 対象のポジションのtpを新しくオーダーするslにする
                                #    sl = position[10] + 0.027  # 対象のポジションのtpをオーダー時の価格+270にする
                                    #tp = position[11] + 0.003  # 対象のポジションのslを新しくオーダーするtpにする
                                    tp = price - 0.01
                                    sl = price + 0.55
                                    magic = 222222
                                    comment = "rapid_change_bid"
                                    settlementFlag = True
                                    message = request(settle_type=settle_type, price=price, sl=sl, tp=tp, magic=magic,comment=comment)
                                    print("rapid_change bid:", message)

            #***************************
            # 222221(買い)を持っていないときの処理
            #***************************
            if magicNo_flag_222221 == False:  # 222221所持フラグがFalseの時に処理をする
                settlementFlag = False
                for position in positions:  # 保有ポジション分処理を回す
                    profit = position[15]  # 利益
                    magicNo = position[6]  # マジックナンバー

                    if profit < 0 and magicNo != 222221:  # 利益が-100以下の場合かつ保有ポジションのマジックナンバーが222222以外の時
                        identifier = position[7]  # 識別子
                        if not identifier in rapid_change_identifiers:  # 識別子が配列の中にない場合(処理をまだ行っていない)
                            position_type = position[5]  # 対象のポジションのオーダータイプ
                            if position_type == 1:
                                if settlementFlag == False:
                                    settle_type = 0  # 送信するオーダータイプ(買い)
                                    price = mt5.symbol_info_tick(symbol).ask
                                 #   sl = position[12] - 0.003  # 対象のポジションのtpを新しくオーダーするslにする
                                #    sl = position[10] - 0.027  # 対象のポジションのtpをオーダー時の価格-270にする
                                    #tp = position[11] - 0.003  # 対象のポジションのslを新しくオーダーするtpにする
                                    tp = price + 0.01
                                    sl = price - 0.55
                                    magic = 222221
                                    comment = "rapid_change_ask"
                                    settlementFlag = True
                                    message = request(settle_type=settle_type,  price=price, sl=sl, tp=tp, magic=magic, comment=comment)
                                    print("rapid_change ask:",message)

    if not positions:  # 保有ポジションがないとき
        rapid_change_identifiers = []  # 識別子リストを空にする

    min1_price_bid = price_bid


def request(settle_type, price, sl, tp, magic, comment):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": settle_type,
#        "position": identifier,
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
    print(comment, request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        message = "2. order_send failed, retcode={}".format(result.retcode)
    else:
        message = "rapid_changeリクエスト送信完了"
    return message

def prompt_request(settle_type, price, magic, comment, identifier):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": settle_type,
        "position": identifier,
        "price": price,  # 現在の価格,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(comment, request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        message = "2. order_send failed, retcode={}".format(result.retcode)
    else:
        message = comment + "リクエスト送信完了"
    return message



if __name__ == '__main__':
    order_up_down_settle()