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
import chromedriver_binary
import datetime
from playsound import playsound

#**********************取得関係宣言********************
#為替　ドル円リアルタイムチャート
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Chrome()
FX_SCREENER =  'https://jp.tradingview.com/forex-screener/'
FX_SCREENER_USDJPY = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(49) > td:nth-child(2) > span'
FX_SCREENER_GBPJPY = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(31) > td:nth-child(2) > span'

USDJPY_TECHNICALS = 'https://jp.tradingview.com/symbols/USDJPY/technicals/'
GBPJPY_TECHNICALS = 'https://jp.tradingview.com/symbols/GBPJPY/technicals/'
TECHNICALS_1MIN_BTN_CSS = '#technicals-root > div > div > div.wrap-2taoBjQZ > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > div > div:nth-child(1)'
TECHNICALS_5MIN_BTN_CSS = '#technicals-root > div > div > div.wrap-2taoBjQZ > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > div > div:nth-child(2)'
TECHNICALS_15MIN_BTN_CSS = '#technicals-root > div > div > div.wrap-2taoBjQZ > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > div > div:nth-child(3)'
TECHNICALS_60MIN_BTN_CSS = '#technicals-root > div > div > div.wrap-2taoBjQZ > div > div > div.scrollWrap-nAnkzkWd.noScrollBar-34JzryqI > div > div > div:nth-child(4)'
TECHNICALS_OCI_BID_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(1) > div.countersWrapper-1TsBXTyc > div:nth-child(1) > span.counterNumber-3l14ys0C.sellColor-2qa8ZOVt'
TECHNICALS_OCI_NEUTRAL_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(1) > div.countersWrapper-1TsBXTyc > div:nth-child(2) > span.counterNumber-3l14ys0C.neutralColor-15OoMFX9'
TECHNICALS_OCI_ASK_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(1) > div.countersWrapper-1TsBXTyc > div:nth-child(3) > span.counterNumber-3l14ys0C.buyColor-4BaoBngr'
TECHNICALS_REMOVE_BID_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(3) > div.countersWrapper-1TsBXTyc > div:nth-child(1) > span.counterNumber-3l14ys0C.sellColor-2qa8ZOVt'
TECHNICALS_REMOVE_NEUTRAL_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(3) > div.countersWrapper-1TsBXTyc > div:nth-child(2) > span.counterNumber-3l14ys0C.neutralColor-15OoMFX9'
TECHNICALS_REMOVE_ASK_CSS = '#technicals-root > div > div > div.speedometersContainer-1EFQq-4i > div:nth-child(3) > div.countersWrapper-1TsBXTyc > div:nth-child(3) > span.counterNumber-3l14ys0C.buyColor-4BaoBngr'

MARKET_INDEX = 'https://jp.tradingview.com/markets/indices/quotes-major/'
MARKET_INDEX_NI225_CSS = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(10) > td:nth-child(2) > span'
MARKET_INDEX_SPX_CSS = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(1) > td:nth-child(2) > span'
MARKET_INDEX_UKX_CSS = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(6) > td:nth-child(2) > span'
MARKET_INDEX_VIX_CSS = '#js-screener-container > div.tv-screener__content-pane > table > tbody > tr:nth-child(4) > td:nth-child(2) > span'

MARKET_INDEX_SPX_RATIO = 0
MARKET_INDEX_NI225_RATIO = 0
MARKET_INDEX_UKX_RATIO = 0
MARKET_INDEX_VIX_RATIO = 0
#**********************取得関係宣言********************

#**********************lineチャットボット***************
line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
def Line_bot(message):  # lineチャットボット
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
#**********************lineチャットボット***************

#**********************前回との比率計算*****************
def ratio_calc(after, before):
    res = (after / before * 100) - 100 # 例 110/100 = 1.1
    res = round(res, 4)
    return res

#**********************前回との比率計算++***************

#**********************ループ前準備*********************

#driver.get(FX_SCREENER)  # URLに遷移

DT_NOW = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')  # 現在時刻
list_max = 15  # (list_max × sleep) の周期で監視する
list = list_max + 1 # 要素数
list_push = 0
warn_diff = 0.15 # 警報を出す基準値
warn_diff2 = -0.15 # 警報を出す基準値
sleep = 60  # スリーブ時間(秒)
minute = (list_max)*sleep/60
second = (list_max)*sleep
# 警報は(list_max * sleep)秒前時になる
print('警報は約', (list_max)*sleep,'秒前-約',minute,'分前の時間と比較して基準',warn_diff,warn_diff2,'を超えていた場合に表示します')
Line_bot(DT_NOW+'\n警報は約'+ str(second) +'秒前-約'+ str(minute) +'分前の時間と比較して基準'+ str(warn_diff) + 'または' + str(warn_diff2)+'を超えていた場合に表示します')
diff_flag = False  # 1週目は警報を出さないようにするためにフラグを設定する
write_flag = False  # -分後の値を書き込むかフラグ

usdjpy_list = [000.000]*(list)  # 000.000で埋めたリストを用意
gbpjpy_list = [000.000]*(list)

for i in range(3):
    driver.execute_script('window.open()')  # 新しいタブを追加でrenge-1個作成する

driver.switch_to.window(driver.window_handles[0])  # 1個目のタブに切り替える
driver.get(FX_SCREENER)  # FXスクリーナー
time.sleep(1)

driver.switch_to.window(driver.window_handles[1])  # 2個目のタブに切り替える
driver.get(USDJPY_TECHNICALS)  # ドル円テクニカル
TECHNICALS_1MIN_BTN = driver.find_element_by_css_selector(TECHNICALS_15MIN_BTN_CSS)
TECHNICALS_1MIN_BTN.click()  #あらかじめ取得範囲にボタンを設定しておく
time.sleep(1)

driver.switch_to.window(driver.window_handles[2])  # 3個目のタブに切り替える
driver.get(GBPJPY_TECHNICALS)  # ポンド円テクニカル
TECHNICALS_1MIN_BTN = driver.find_element_by_css_selector(TECHNICALS_15MIN_BTN_CSS)
TECHNICALS_1MIN_BTN.click()  #あらかじめ取得範囲にボタンを設定しておく
time.sleep(1)

driver.switch_to.window(driver.window_handles[3])  # 4個目のタブに切り替える
driver.get(MARKET_INDEX)  # マーケット指数
time.sleep(1)
#**********************ループ前準備*********************

#**********************書き込み関係宣言********************
"""WRITE_DATA = [DT_NOW, USDJPY_RATE, GBPJPY_RATE,
                         USDJPY_TECHNICALS_OCI_BID,USDJPY_TECHNICALS_OCI_NEUTRAL, USDJPY_TECHNICALS_OCI_ASK,
                         USDJPY_TECHNICALS_REMOVE_BID, USDJPY_TECHNICALS_REMOVE_NEUTRAL, USDJPY_TECHNICALS_REMOVE_ASK,
                         GBPJPY_TECHNICALS_OCI_BID, GBPJPY_TECHNICALS_OCI_NEUTRAL, GBPJPY_TECHNICALS_OCI_ASK,
                         GBPJPY_TECHNICALS_REMOVE_BID, GBPJPY_TECHNICALS_REMOVE_NEUTRAL, GBPJPY_TECHNICALS_REMOVE_ASK,
                         MARKET_INDEX_SPX, MARKET_INDEX_NI225, MARKET_INDEX_UKX, MARKET_INDEX_VIX,
                         USDJPY_AFTER_RATE, GBPJPY_AFTER_RATE ] * list"""

#**********************書き込み関係宣言********************

#**********************為替取得ドル円ポンド円*************

with open('為替情報.csv',mode='a',encoding='shift_jis') as f:
    # **********************雑処理定義*********************
    writer_line = csv.writer(f, lineterminator='\n')  # 書き込み時末尾が改行
    writer = csv.writer(f, lineterminator=',')  # 書き込み時末尾がカンマ
    # **********************雑処理定義*********************
    while True:
        try:
            driver.switch_to.window(driver.window_handles[0])  # 1個目のタブに切り替える
            DT_NOW = datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S')  # 現在時刻
            print('開始',sleep,'秒間隔に計算します',DT_NOW)

            # USDJPYレート取得
            fxscreener_html = driver.page_source  # DRIVERのページのソースを取得
            fxscreener_soup = BeautifulSoup(fxscreener_html, "html.parser")  # Beautifulsoup形式に変換
            USDJPY_RATE = fxscreener_soup.select_one(FX_SCREENER_USDJPY).string  #USDJPYのレートを抽出
            print(USDJPY_RATE)
            usdjpy_list[list_push] = float(USDJPY_RATE)  # リストに順番にレートを入れる
            # USDJPYレート取得

            # GBPJPYレート取得
            GBPJPY_RATE = fxscreener_soup.select_one(FX_SCREENER_GBPJPY).string
            print(GBPJPY_RATE)
            gbpjpy_list[list_push] = float(GBPJPY_RATE)  # リストに順番にレートを入れる
            # GBPJPYレート取得

            print(usdjpy_list,'\n' ,gbpjpy_list)

            #time.sleep(sleep)  # sleep秒休む
        #--------------ここより下はウェイト中に処理を実行することで効率よく処理できる

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

            print(list_push,minute,'分前のレート差額:usdjpy', usdjpy_diff)
            print(minute,'分前のレート差額:gbpjpy', gbpjpy_diff)


            if diff_flag:  # リストが埋まるまでは差額を計算しない
                usdjpy_now = ('{:.03f}'.format(usdjpy_diff))
                gbpjpy_now = ('{:.03f}'.format(gbpjpy_diff))
                if usdjpy_diff > warn_diff:   #usdjpyの--分前とのレート差が基準以上あるとき
                    print('差額が',warn_diff,'を超えていますusdjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分:usdjpy差額:\n'+ str(usdjpy_before)
                             + '⇒' + str(usdjpy_list[list_push]) + '\n' + usdjpy_now + '円上昇しました')
                    playsound('itemget4.mp3')

                if usdjpy_diff < warn_diff2:
                    print('差額が',warn_diff2,'を超えていますusdjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のusdjpy差額:\n'+ str(usdjpy_before)
                             + '⇒' + str(usdjpy_list[list_push]) + '\n' + usdjpy_now + '円下降しました')
                    playsound('itemget4.mp3')

                if gbpjpy_diff > warn_diff:   #gbpjpyの--分前とのレート差が基準以上あるとき:
                    print('差額が',warn_diff,'を超えていますgbpjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のgbpjpy差額:\n' + str(gbpjpy_before)
                             + '⇒' + str(gbpjpy_list[list_push]) + '\n' + gbpjpy_now + '円上昇しました')
                    playsound('itemget4.mp3')

                if gbpjpy_diff < warn_diff2:
                    print('差額が',warn_diff2,'を超えていますgbpjpy')
                    Line_bot(DT_NOW + '\n' + str(minute) + '分のgbpjpy差額:\n' + str(gbpjpy_before)
                             + '⇒' + str(gbpjpy_list[list_push]) + '\n' + gbpjpy_now + '円下降しました')
                    playsound('itemget4.mp3')
        #**********************為替取得ドル円ポンド円*************

        #*******************--分後の為替(目的変数)を書きこみ*******
            if write_flag:  # 2行目以降書き込み
                writer.writerow([usdjpy_before, gbpjpy_before])  # (sleep×list数)秒前のドル円、ポンド円として前回の行に書き込む
                writer_line.writerow([USDJPY_RATE, GBPJPY_RATE])  # sleep秒後のドル円、ポンド円として前回の行に書き込む
                f.flush()  # 無限ループ中はflushで強制書き込みを行う
        #*******************--分後の為替(目的変数)を書きこみ*******

        #**********************オシレーター移動平均取得ドル円*******
            driver.switch_to.window(driver.window_handles[1])  # ドル円テクニカルタブに切り替える
            driver.refresh()
            TECHNICALS_1MIN_BTN = driver.find_element_by_css_selector(TECHNICALS_1MIN_BTN_CSS)
            driver.implicitly_wait(3)
            TECHNICALS_1MIN_BTN.click()  # あらかじめ取得範囲にボタンを設定しておく
            driver.implicitly_wait(3)
            USDJPY_TECHNICALS_html = driver.page_source  # DRIVERのページのソースを取得
            USDJPY_TECHNICALS_soup = BeautifulSoup(USDJPY_TECHNICALS_html, "html.parser")  # Beautifulsoup形式に変換

            USDJPY_TECHNICALS_OCI_BID = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_BID_CSS).string
            USDJPY_TECHNICALS_OCI_NEUTRAL = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_NEUTRAL_CSS).string
            USDJPY_TECHNICALS_OCI_ASK = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_ASK_CSS).string

            USDJPY_TECHNICALS_REMOVE_BID = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_BID_CSS).string
            USDJPY_TECHNICALS_REMOVE_NEUTRAL = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_NEUTRAL_CSS).string
            USDJPY_TECHNICALS_REMOVE_ASK = USDJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_ASK_CSS).string
        #**********************オシレーター移動平均取得ドル円*******

        # **********************オシレーター移動平均取得ポンド円*****
            driver.switch_to.window(driver.window_handles[2])  # ポンド円テクニカルタブに切り替える
            driver.refresh()
            TECHNICALS_1MIN_BTN = driver.find_element_by_css_selector(TECHNICALS_1MIN_BTN_CSS)
            driver.implicitly_wait(3)
            TECHNICALS_1MIN_BTN.click()  # あらかじめ取得範囲にボタンを設定しておく
            driver.implicitly_wait(3)
            time.sleep(1)
            GBPJPY_TECHNICALS_html = driver.page_source  # DRIVERのページのソースを取得
            GBPJPY_TECHNICALS_soup = BeautifulSoup(GBPJPY_TECHNICALS_html, "html.parser")  # Beautifulsoup形式に変換

            GBPJPY_TECHNICALS_OCI_BID = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_BID_CSS).string
            GBPJPY_TECHNICALS_OCI_NEUTRAL = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_NEUTRAL_CSS).string
            GBPJPY_TECHNICALS_OCI_ASK = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_OCI_ASK_CSS).string

            GBPJPY_TECHNICALS_REMOVE_BID = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_BID_CSS).string
            GBPJPY_TECHNICALS_REMOVE_NEUTRAL = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_NEUTRAL_CSS).string
            GBPJPY_TECHNICALS_REMOVE_ASK = GBPJPY_TECHNICALS_soup.select_one(TECHNICALS_REMOVE_ASK_CSS).string
        # **********************オシレーター移動平均取得ポンド円*****

        # **********************マーケット指数********************
            if write_flag:  # 2行目以降代入する
                MARKET_INDEX_SPX_BEFORE = MARKET_INDEX_SPX
                MARKET_INDEX_NI225_BEFORE = MARKET_INDEX_NI225
                MARKET_INDEX_UKX_BEFORE = MARKET_INDEX_UKX
                MARKET_INDEX_VIX_BEFORE = MARKET_INDEX_VIX

            driver.switch_to.window(driver.window_handles[3])  # マーケット指数タブに切り替える
            driver.refresh()
            driver.implicitly_wait(3)
            time.sleep(1)      
            MARKET_INDEX_html = driver.page_source  # DRIVERのページのソースを取得
            MARKET_INDEX_soup = BeautifulSoup(MARKET_INDEX_html, "html.parser")  # Beautifulsoup形式に変換

            MARKET_INDEX_SPX = MARKET_INDEX_soup.select_one(MARKET_INDEX_SPX_CSS).string
            MARKET_INDEX_NI225 = MARKET_INDEX_soup.select_one(MARKET_INDEX_NI225_CSS).string
            MARKET_INDEX_UKX = MARKET_INDEX_soup.select_one(MARKET_INDEX_UKX_CSS).string
            MARKET_INDEX_VIX = MARKET_INDEX_soup.select_one(MARKET_INDEX_VIX_CSS).string

        # **********************マーケット指数********************
        # **********************計算&書き込み処理********************
            if write_flag:  # 2行目以降代入する
                MARKET_INDEX_SPX_RATIO = ratio_calc(float(MARKET_INDEX_SPX), float(MARKET_INDEX_SPX_BEFORE))
                MARKET_INDEX_NI225_RATIO = ratio_calc(float(MARKET_INDEX_NI225), float(MARKET_INDEX_NI225_BEFORE))
                MARKET_INDEX_UKX_RATIO = ratio_calc(float(MARKET_INDEX_UKX), float(MARKET_INDEX_UKX_BEFORE))
                MARKET_INDEX_VIX_RATIO = ratio_calc(float(MARKET_INDEX_VIX), float(MARKET_INDEX_VIX_BEFORE))

            writer.writerow([DT_NOW, USDJPY_RATE, GBPJPY_RATE,
                             USDJPY_TECHNICALS_OCI_ASK,USDJPY_TECHNICALS_OCI_NEUTRAL, USDJPY_TECHNICALS_OCI_BID,
                             USDJPY_TECHNICALS_REMOVE_ASK, USDJPY_TECHNICALS_REMOVE_NEUTRAL, USDJPY_TECHNICALS_REMOVE_BID,
                             GBPJPY_TECHNICALS_OCI_ASK, GBPJPY_TECHNICALS_OCI_NEUTRAL, GBPJPY_TECHNICALS_OCI_BID,
                             GBPJPY_TECHNICALS_REMOVE_ASK, GBPJPY_TECHNICALS_REMOVE_NEUTRAL, GBPJPY_TECHNICALS_REMOVE_BID,
                             MARKET_INDEX_SPX,MARKET_INDEX_SPX_RATIO, MARKET_INDEX_NI225, MARKET_INDEX_NI225_RATIO,
                             MARKET_INDEX_UKX, MARKET_INDEX_UKX_RATIO, MARKET_INDEX_VIX, MARKET_INDEX_VIX_RATIO])
            f.flush()
            print([DT_NOW, USDJPY_RATE, GBPJPY_RATE,
                             USDJPY_TECHNICALS_OCI_ASK,USDJPY_TECHNICALS_OCI_NEUTRAL, USDJPY_TECHNICALS_OCI_BID,
                             USDJPY_TECHNICALS_REMOVE_ASK, USDJPY_TECHNICALS_REMOVE_NEUTRAL, USDJPY_TECHNICALS_REMOVE_BID,
                             GBPJPY_TECHNICALS_OCI_ASK, GBPJPY_TECHNICALS_OCI_NEUTRAL, GBPJPY_TECHNICALS_OCI_BID,
                             GBPJPY_TECHNICALS_REMOVE_ASK, GBPJPY_TECHNICALS_REMOVE_NEUTRAL, GBPJPY_TECHNICALS_REMOVE_BID,
                             MARKET_INDEX_SPX, MARKET_INDEX_SPX_RATIO, MARKET_INDEX_NI225, MARKET_INDEX_NI225_RATIO,
                             MARKET_INDEX_UKX, MARKET_INDEX_UKX_RATIO, MARKET_INDEX_VIX, MARKET_INDEX_VIX_RATIO])
        # **********************計算&書き込み処理********************

            write_flag = True
            #time.sleep(5)  # 30秒休む
            list_push += 1
            if list_push == list_max + 1:  # カウンタがmaxをこえたら0に戻す
                list_push = 0
                diff_flag = True
            time.sleep(sleep)  # sleep秒休む
        except:
            print('******トライ発動******')
            pass
