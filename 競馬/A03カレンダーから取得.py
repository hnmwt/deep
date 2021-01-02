
#**********************************************
#
#アウトプット:カレンダーから取得フォルダのDatabase_Horse.csv
#
#**********************************************
#グローバル変数　取得したい月日のurlを入力する
Month_url = "https://race.netkeiba.com/top/calendar.html?year=2020&month=1"  #20年1月
#----------------------------------------------------------------------------------


Hanyou_url = "https://race.netkeiba.com/"

from bs4 import BeautifulSoup
import requests
import time
import selenium.webdriver
from selenium import webdriver

#---------------------------
#機能 urlからsoupを作成する
#引数 url
#戻り値 soup
#---------------------------
def response(Month_url):
    from bs4 import BeautifulSoup
    import requests
    response = requests.get(Month_url)  # urlを指定
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')  # soupを使い抽出していく
    return soup

#---------------------------
#機能 selectorからリンクを抽出する
#引数 selector
#戻り値 link
#---------------------------
def Get_selector(selector,soup):
    selector_Cal = soup.select(selector)  # セレクターを取得
    if selector_Cal != []:  # 取得できるとき
        for a in selector:  # forを回す
            link = a.attrs['href']  # リンクを取得(a.attrs['href]は構文のようなもの??)
    return link


#---------------------------
#機能 カレンダーから日にちごとのリンクを抽出する
#引数 無し
#戻り値 無し
#---------------------------
def Calender():    # カレンダーから日ごとの開催レースurlを取得
    soup = response(Month_url)
    for row in range(2, 7):  #カレンダーの行を指定(2-6)
        for column in range(1, 8):  #カレンダーの列を指定(1-7)
            # カレンダー中の開催競馬のurl
            selector_Cal = "#Netkeiba_RaceTop > div.Wrap.fc > div > div.Main_Column > div > div > div.Race_Calendar_Main > table > tbody > tr:nth-child(" + str(row) + ") > td:nth-child(" + str(column) + ") > a"
            selector_Cal = soup.select(selector_Cal)  # セレクターを取得
            if selector_Cal != []:  # 取得できるとき
                for a in selector_Cal:  # forを回す
                    link = a.attrs['href']  # リンクを取得(a.attrs['href]は構文のようなもの??)
                    link_Race_Itiran = Hanyou_url + link[3:]
                    #print(link_Race_Itiran)
                Race_Kobetsu(link_Race_Itiran)
        print("row:",str(row), "column:",str(column), "終了")


#---------------------------
#機能 日にちごとのレースからリンクを抽出する(calenderから呼び出し)
#引数 日にちごとのレース
#戻り値 無し
#---------------------------
def Race_Kobetsu(link_Race_Itiran):  # 開催レースからurlをcsvに格納

    soup = response(link_Race_Itiran)
    with open("カレンダーから取得/aタグ.txt", mode="a", encoding='utf-8') as f:
        driver = webdriver.Chrome()
        driver.get(link_Race_Itiran)
        time.sleep(3)
        #for Where in range(1, 4):  # 開催レースの行(場所)を指定(1-3)
            #for Round in range(1, 13):  # 開催レースの列(ラウンド)を指定(1-12)
        elems = driver.find_elements_by_tag_name('a') #aタグを検索
        for e in elems:
            e = e.get_attribute('href')
            print(e)
            f.write(str(e)+'\n')
        driver.quit()

#---------------------------
#機能 日にちごとのレースで作成したcsvから対象のレースだけを抽出してcsvにする
#引数 無し
#戻り値 無し
#---------------------------
def Seikei():#Race_kobetsuで作成したaタグ取得のcsvからレースのurlを抜き出す
    kyoutuu = "https://race.netkeiba.com/race/result.html?race_id="
    with open("カレンダーから取得/aタグ.txt", mode="r", encoding='utf-8') as f:
        for row in f:
            if row.startswith(kyoutuu):
                File = open("カレンダーから取得/レースURL.txt", mode="a", encoding='utf-8')
                File.write(str(row) + '\n')
                File.close()
                print('書き込みました:{}'.format(row))
    print('ファイルを作成しました')

#---------------------------
#機能 対象のレースだけを抽出したcsvを一つのcsvにする(各月ごとに実行してデータをDatabase.csvに集約)
#引数 無し
#戻り値 無し
#---------------------------
def Matome():
    Racedata_Month = "202010レースURL.txt"
    with open("カレンダーから取得/" + Racedata_Month , mode='r', encoding='utf-8') as f_Calender:
        with open('Database_Horse.csv', mode='a', encoding='utf-8') as f:
            for row in f_Calender:
                row = row.rstrip()
                if row != "":       #""以外の時書き込み
                    print(row)
                    f.write(row + '\n')
    print(Racedata_Month,'完了')



# aタグのcsvを作成
Calender()
# calenderで作ったcsvを整形
Seikei()
"""import selenium.webdriver

driver = selenium.webdriver.PhantomJS()
driver.get('https://race.netkeiba.com/top/race_list.html?kaisai_date=20200105')
elems = driver.find_elements_by_tag_name('a')
for e in elems:
    print(e.get_attribute('href'))"""

