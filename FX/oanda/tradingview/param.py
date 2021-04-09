#LIVE = True # 本番口座
LIVE = False # デモ口座
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