#**********************MEMO***************************
# 60秒ごとにデータを出力すると1日で1440行
#
#**********************MEMO***************************
from bs4 import BeautifulSoup
import requests
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import random
import datetime
import chromedriver_binary
import datetime

#**********************グローバル宣言********************
#為替　ドル円リアルタイムチャート
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

usdjpy_url = 'https://jp.tradingview.com/symbols/USDJPY/'
usdjpy_selector = '#js-category-content > div > div > div > div > div.tv-card-container__chart > div > div.tv-feed-widget-chart__container-wrapper > div.js-feed-widget-chart-control-container.tv-feed-widget-chart__top-control > div > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > label.option-1dETGYkD.optionSelected-3RZc8o2i.mainOption-3oBhRfoE > div > div.tabValue-3iOTI9jm'
gbpjpy_url = 'https://jp.tradingview.com/symbols/GBPJPY/'
gbpjpy_selector = '#js-category-content > div > div > div > div > div.tv-card-container__chart > div > div.tv-feed-widget-chart__container-wrapper > div.js-feed-widget-chart-control-container.tv-feed-widget-chart__top-control > div > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > label.option-1dETGYkD.optionSelected-3RZc8o2i.mainOption-3oBhRfoE > div > div.tabValue-3iOTI9jm'
FX_SCREENER =  'https://jp.tradingview.com/forex-screener/'
FX_SCREENER_USDJPY = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(49) > td:nth-child(2) > span'
FX_SCREENER_GBPJPY = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(31) > td:nth-child(2) > span'
#**********************グローバル宣言********************

#**********************lineチャットボット***************
line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
def Line_bot(message):  # lineチャットボット
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
#**********************lineチャットボット***************

#**********************ループ前準備*********************
driver.execute_script('window.open()')  # 新しいタブを作成する
driver.switch_to.window(driver.window_handles[0])  # 1個目のタブに切り替える
driver.get(usdjpy_url)  # URLに遷移
driver.switch_to.window(driver.window_handles[1])  # 2個目のタブに切り替える
driver.get(gbpjpy_url)  # URLに遷移
DT_NOW = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')  # 現在時刻
list_max = 19  # リストに代入する要素のカウンタ(0～19までの20通り)
list_push = 0
warn_diff = 0.1 # 警報を出す基準値
warn_diff2 = -0.1 # 警報を出す基準値
sleep = 30  # スリーブ時間(秒)
minute = (list_max+1)*sleep/60
# 警報は(list_max * sleep)秒前時になる
print('警報は約', (list_max+1)*sleep,'秒前-約',minute,'分前の時間と比較して基準',warn_diff,warn_diff2,'を超えていた場合に表示します')
Line_bot(DT_NOW+'\n警報は約'+ str((list_max+1)*sleep) +'秒前-約'+ str((list_max+1)*sleep/60) +'分前の時間と比較して基準'+ str(warn_diff) + 'もしくは' + str(warn_diff2)+'を超えていた場合に表示します')
diff_flag = False  # 最初の10分館は警報を出さないようにするためにフラグを設定する

usdjpy_list = [000.000]*(list_max + 1)  # 000.000で埋めたリストを用意
gbpjpy_list = [000.000]*(list_max + 1)
#**********************ループ前準備*********************

try:
    with open('為替情報.csv',mode='a',encoding='shift_jis') as f:
        while True:
            DT_NOW = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')  # 現在時刻
            print('開始',sleep,'秒間隔に計算します',DT_NOW)
            # USDJPYレート取得
            driver.switch_to.window(driver.window_handles[0]) # 1個目のタブに切り替える
            usdjoy_html = driver.page_source  # DRIVERのページのソースを取得
            usdjoy_soup = BeautifulSoup(usdjoy_html, "html.parser")  # Beautifulsoup形式に変換
            USDJPY_RATE = usdjoy_soup.select_one(usdjpy_selector).string  #bUSDJPYのレートを抽出
            print(USDJPY_RATE)
            usdjpy_list[list_push] = float(USDJPY_RATE)  # 20までのリストに順番にレートを入れる
            # USDJPYレート取得

            # GBPJPYレート取得
            driver.switch_to.window(driver.window_handles[1]) # 2個目のタブに切り替える
            gbpjpy_html = driver.page_source  # DRIVERのページのソースを取得
            gbpjpy_soup = BeautifulSoup(gbpjpy_html, "html.parser")  # Beautifulsoup形式に変換
            GBPJPY_RATE = gbpjpy_soup.select_one(gbpjpy_selector).string
            print(GBPJPY_RATE)
            gbpjpy_list[list_push] = float(GBPJPY_RATE)  # 20までのリストに順番にレートを入れる
            # GBPJPYレート取得

            print(usdjpy_list,'\n' ,gbpjpy_list)

            #time.sleep(sleep)  # sleep秒休む
        #--------------ここより下はウェイト中に処理を実行することで効率よく処理できる
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([DT_NOW, USDJPY_RATE, GBPJPY_RATE])
            f.flush()  # 無限ループ中はflushで強制書き込みを行う

            if list_push == list_max:  # 要素が最後の時は0番目との差額を計算することで--分前との差額を算出する
                usdjpy_diff = usdjpy_list[list_push] - usdjpy_list[0]
                gbpjpy_diff = gbpjpy_list[list_push] - gbpjpy_list[0]

                usdjpy_before = usdjpy_list[0]  # --分前の値を代入
                gbpjpy_before = gbpjpy_list[0]

            else:  # それ以外の時は現在の要素+1との差額を計算することで--分前との差額を算出する
                usdjpy_diff = usdjpy_list[list_push] - usdjpy_list[list_push+1]
                gbpjpy_diff = gbpjpy_list[list_push] - gbpjpy_list[list_push+1]

                usdjpy_before = usdjpy_list[list_push+1]  # --分前の値を代入
                gbpjpy_before = gbpjpy_list[list_push+1]

            print(list_push,'10分前のレート差額:usdjpy', usdjpy_diff)
            print('10分前のレート差額:gbpjpy', gbpjpy_diff)

            list_push += 1
            if list_push == list_max+1:  # カウンタが20になったら0に戻す
                list_push = 0
                diff_flag = True

            if diff_flag:  # 1週目はカウントしない
                usdjpy_now = ('{:.03f}'.format(usdjpy_diff))
                gbpjpy_now = ('{:.03f}'.format(gbpjpy_diff))
                if usdjpy_diff > warn_diff:   #usdjpyの--分前とのレート差が基準以上あるとき
                    print('差額が',warn_diff,'を超えていますusdjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分:usdjpy差額:'+ str(usdjpy_list[list_push])
                             + '⇒' + str(usdjpy_before) + '\n' + usdjpy_now + '円上昇しました')
                if usdjpy_diff < warn_diff2:
                    print('差額が',warn_diff2,'を超えていますusdjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のusdjpy差額:'+ str(usdjpy_list[list_push])
                             + '⇒' + str(usdjpy_before) + '\n' + usdjpy_now + '円下降しました')

                if gbpjpy_diff > warn_diff:   #gbpjpyの--分前とのレート差が基準以上あるとき:
                    print('差額が',warn_diff,'を超えていますgbpjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のusdjpy差額:' + str(gbpjpy_list[list_push])
                             + '⇒' + str(gbpjpy_before) + '\n' + gbpjpy_now + '円上昇しました')
                if gbpjpy_diff < warn_diff2:
                    print('差額が',warn_diff2,'を超えていますgbpjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のusdjpy差額:' + str(gbpjpy_list[list_push])
                             + '⇒' + str(gbpjpy_before) + '\n' + gbpjpy_now + '円下降しました')

            #time.sleep(5)  # 30秒休む
            time.sleep(sleep)  # sleep秒休む
except:
    print(('エラー'))
finally:
    print('終了')
    Line_bot('終了しました')
#driver.close()