import datetime

LIVE = True # 本番口座
#LIVE = False # デモ口座
#EA = True
EA = False
if LIVE == True:
    account_ID = 900006047
    password = "Hnm4264wtr"
    print("本番口座です")
elif LIVE == False:
    account_ID = 400019080
    password = "Hnm4264wtr"
    print("demo口座です")

symbol = "USDJPY"
deviation = 10
lot = 0.1  # ロット数

day_of_order_time = datetime.timedelta(hours=10, minutes=00)  # 1日に一度注文する時間
day_of_order_time_hour = 10
day_of_order_time_minute = 0

print(day_of_order_time)