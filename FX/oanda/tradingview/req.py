import MetaTrader5 as mt5
import param

deviation = param.deviation
lot = param.lot
symbol = param.symbol


def normal_request(settle_type, price, magic, comment):  # tp,sl指定なし新規注文
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": settle_type,
       # "position": identifier,
        "price": price,  # 現在の価格,
        "tp": 40,  # --------------------後で廃止
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

def settlement_request(settle_type, price, magic, comment, identifier):  # 決済
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