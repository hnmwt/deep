import MetaTrader5 as mt5
import param

deviation = param.deviation
lot = param.lot
symbol = param.symbol

Buy = 0
Sell = 1


def set_tp(price, order_type, value):
    if order_type == Buy:
        tp = price + value
    elif order_type == Sell:
        tp = price - value
    return tp

def set_sl(price, order_type, value):
    if order_type == Buy:
        sl = price - value
    elif order_type == Sell:
        sl = price + value
    return sl


def normal_request(settle_type, price, magic, comment, tp=0.08, sl=0.5):  # 新規注文
    #   mt5.initialize()
    #   value = 0.08
    tp = set_tp(price, settle_type, tp)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": settle_type,
        # "position": identifier,
        "price": price,  # 現在の価格,
        "tp": tp,  # --------------------後で廃止
        "sl": sl,
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
    print(message)
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
