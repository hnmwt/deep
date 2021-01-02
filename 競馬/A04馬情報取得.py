import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#------グローバル----------------
now = datetime.datetime.now()
Datetime_now = now.strftime("%Y%m%d%H%M%S")
Horse_name = []
URL_LIST = []
driver = webdriver.Chrome()
Tyokyo_URL_MATCH = []
Tyokyo_HEADURL = 'https://db.netkeiba.com/'
#------グローバル----------------

#---------------------------
#機能 馬の過去5回戦の情報をcsv化する
#引数 競走馬データページ
#戻り値 無し
#---------------------------
def Get_Data(url):
#デバッグ用
   #  driver = webdriver.Chrome()
   #  options = Options()
   #  options.binary_location = 'https://www.netkeiba.com/?rf=logo'
   #  driver.get('https://regist.netkeiba.com/account/?pid=login')
   #  time.sleep(1)
   #  # ID/PASSを入力
   #  id = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > table > tbody > tr:nth-child(1) > td > input[type=text]')
   #  id.send_keys("hnmwtr927@gmail.com")
   #  password = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > table > tbody > tr:nth-child(2) > td > input[type=password]')
   #  password.send_keys("hnm4264wtr")
   #
   #  time.sleep(1)
   #
   #  # ログインボタンをクリック
   #  login_button = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > input[type=image]:nth-child(6)')
   #  login_button.click()
   #  time.sleep(1)
#デバッグ用



    #beautifulsoupログイン用
 #    USER = "hnmwtr927@gmail.com"
 #    PASSWORD = "hnm4264wtr"
 #    login_info = {
 #        "user_login_id":USER,
 #        "passwprd_pswd":PASSWORD
 #    }
 #    session = requests.session()
 #    url_login = "https://regist.netkeiba.com/account/?pid=login"
 #    res = session.post(url_login, data=login_info)
 #    print(res.text)
    #beautifulsoupログイン用


     driver.get(url)
     soup = BeautifulSoup(driver.page_source, 'html.parser') # 現在表示しているページのソースを取得
     time.sleep(1)

     Tyokyo_css = '#db_main_box > div > div.db_head_regist.fc > ul > li:nth-child(7) > a'
     Tyokyo_link = soup.select(Tyokyo_css)
     for a in Tyokyo_link:
        Tyokyo_url = a.attrs['href']  # リンクを取得(a.attrs['href]は構文のようなもの??)
        #Tyokyo_URL_MATCH.append(Tyokyo_url)
     Tyokyo_url = Tyokyo_HEADURL + Tyokyo_url
     driver.get(Tyokyo_url)
     soup_Tyokyo = BeautifulSoup(driver.page_source, 'html.parser')


#beautifulsoup用
     with open("soup.txt",mode='w',encoding='utf-8') as f_soup:
        form_soup = soup
        form_soup = str(form_soup)
        form_soup.replace(',', '-')
        f_soup.write(str(form_soup))              #soupをテキストに書き込み
     print('soup.txtにパーサーを書き込みました。')
     #time.sleep(1)
     for i in range(1,6): #過去5戦のデータをとる

        d00_Horse_name = '#db_main_box > div.db_head.fc > div.db_head_name.fc > div.horse_title > h1'
        d01_Whattime = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(1) > a"

        d02_Weather = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(3)"
        d03_Round = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(4)"
        d04_Racename ="#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(5) > a"
        d05_Horse_Num = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(7)"
        d06_Wakuban = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(8)"
        d07_Horse_No = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(9)"
        d08_odds = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(10)"
        d09_Fun = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(11)"
        d10_Result = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(12)"
        d11_human = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(13)"
        d12_Kinryo = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(14)"
        d13_Field = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(15)"
        d14_Range = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(15)"
        d15_Ground = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(16)"
        d16_Ground_Index = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:index1.txt_right"
        d17_Time = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(18)"
        d18_Difference = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(19)"
        d19_Time_Index = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:index2.txt_right"
        d20_Passing = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(21)"
        d21_pace = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(22)"
        d22_Up = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(23)"
        d23_Horse_Weight = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(24)"
        d24_Money = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child(" + str(
            i) + ") > td:nth-child(28)"

        #調教データ
        Tyokyo_date = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(1)"
        Tyokyo_where = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(2)"
        Tyokyo_Umaba = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(3)"
        Tyokyo_noriyaku = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(4)"
        Tyokyo_time1 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td.TrainingTimeData.txt_l > ul > li:nth-child(2)"
        Tyokyo_time2 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td.TrainingTimeData.txt_l > ul > li:nth-child(3)"
        Tyokyo_time3 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td.TrainingTimeData.txt_l > ul > li:nth-child(4)"
        Tyokyo_time4 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td.TrainingTimeData.txt_l > ul > li:nth-child(5)"

        Tyokyo_ichi = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(6)"
        Tyokyo_Kyakusyoku = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(7)"
        Tyokyo_Hyouka1 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(8)"
        Tyokyo_Hyouka2 = "#main > ul > li:nth-child(" + str(i) + ") > table > tbody > tr:nth-child(2) > td:nth-child(9)"

        DATA = [
            d00_Horse_name,
            d01_Whattime,
            d02_Weather,
            d03_Round,
            d04_Racename,
            d05_Horse_Num,
            d06_Wakuban,
            d07_Horse_No,
            d08_odds,
            d09_Fun,
            d10_Result,
            d11_human,
            d12_Kinryo,
            d13_Field,
            d14_Range,
            d15_Ground,
            d16_Ground_Index,
            d17_Time,
            d18_Difference,
            d19_Time_Index,
            d20_Passing,
            d21_pace,
            d22_Up,
            d23_Horse_Weight,
            d24_Money,
            Tyokyo_date,
            Tyokyo_where,
            Tyokyo_Umaba,
            Tyokyo_noriyaku,
            Tyokyo_time1,
            Tyokyo_time2,
            Tyokyo_time3,
            Tyokyo_time4,
            Tyokyo_ichi,
            Tyokyo_Kyakusyoku,
            Tyokyo_Hyouka1,
            Tyokyo_Hyouka2
        ]

        def WRITE_TYOKYO():
            Write_data_parser = soup_Tyokyo.select_one(num).string  # セレクター取得
            Write_data_parser_CSV = Write_data_parser.replace(',', '')
            f.write(str(Write_data_parser_CSV) + ',')
            print('調教書き込み', Write_data_parser_CSV)


        with open('Database_Horse_Race' + Datetime_now +'.csv', mode='a', encoding='utf-8') as f:
            for num in DATA:
                try:
                    if num == d16_Ground_Index:                     #馬場指数とタイム指数はsoup.txtから取得
                        with open("soup.txt", mode='r', encoding='utf-8') as f_Index:
                            reader = f_Index.readlines()
                            #reader.replace(',', '-')
                            for i, e in enumerate(reader):  #enumurateはリストの番号と要素を返す
                                if Criteria_Whattime in e:  #開催年月日がリストの中で部分一致するとき
                                    Condition1 = i
                            result = Condition1 + 22        #開催年月日+22行目を決め打ち
                            Write_data_parser_CSV = reader[result]
                            Write_data_parser_CSV = Write_data_parser_CSV.rstrip()
                            f.write(str(Write_data_parser_CSV) + ',')
                            print('1情報書き込み', Write_data_parser_CSV)

                    elif num == d19_Time_Index:                     #馬場指数とタイム指数はsoup.txtから取得
                        with open("soup.txt", mode='r', encoding='utf-8') as f_Index:
                            reader = f_Index.readlines()
                            #reader.replace(',', '-')
                            for i, e in enumerate(reader):
                                if Criteria_Whattime in e:  #開催年月日がリストの中で部分一致するとき
                                    Condition1 = i
                            result = Condition1 + 29        #開催年月日+29行目を決め打ち
                            Write_data_parser_CSV = reader[result]
                            Write_data_parser_CSV = Write_data_parser_CSV.rstrip()
                            f.write(str(Write_data_parser_CSV) + ',')
                            print('1情報書き込み', Write_data_parser_CSV)

                    elif num == Tyokyo_date: # numがDATAの25番目以降(調教タイム)の時
                        WRITE_TYOKYO()
                    elif num == Tyokyo_where:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_Umaba:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_noriyaku:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_time1:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_time2:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_time3:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_time4:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_ichi:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_Kyakusyoku:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_Hyouka1:
                        WRITE_TYOKYO()
                    elif num == Tyokyo_Hyouka2:
                        WRITE_TYOKYO()


                    else:
                        Write_data_parser = soup.select_one(num).string  # セレクター取得
                        Write_data_parser_CSV = Write_data_parser.replace(',','')
                        f.write(str(Write_data_parser_CSV)+',')
                        print('1情報書き込み',Write_data_parser)
                        if num == d01_Whattime:              #開催日時の場合変数に格納して馬場指数、タイム指数に使用する
                            Criteria_Whattime = Write_data_parser_CSV

                except:
                    f.write('取得エラー' + ',')
                    print('1情報書き込み', '取得エラー')
            f.write("\n")
        print("ストップ")







        #time.sleep(random.randint(1, 6))
     #driver.close()

#---------------------------
#機能 ネット競馬にログインする
#引数 無し
#戻り値 無し
#---------------------------
class login():
    options = Options()
    options.binary_location = 'https://www.netkeiba.com/?rf=logo'
    driver.get('https://regist.netkeiba.com/account/?pid=login')
    time.sleep(1)
    # ID/PASSを入力
    id = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > table > tbody > tr:nth-child(1) > td > input[type=text]')
    id.send_keys("hnmwtr927@gmail.com")
    password = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > table > tbody > tr:nth-child(2) > td > input[type=password]')
    password.send_keys("hnm4264wtr")

    time.sleep(1)

    # ログインボタンをクリック
    login_button = driver.find_element_by_css_selector('#contents > div.member_select_box.fc > div.mem_login.wakubox > div.loginbox.fc > form > input[type=image]:nth-child(6)')
    login_button.click()
    time.sleep(1)

#---------------------------
#機能 馬別のページへ遷移する
#引数 無し
#戻り値 無し
#---------------------------
class Data_Collection():
    Horse_URL_MATCH = []
    CountHorseNum = 0
    f = open('Database_Horse.csv', mode='r', encoding='utf-8')
    #-----------1ページ中の処理
    for row in f:
        CountHorseNum += 1  #URLが何個目か(何レース目か)
        row = row.rstrip('\n')  #rowはDatabase_Horse.csvのurl(レースのurl)
        response = requests.get(row)  # 各馬のデータベースurlを指定
        time.sleep(1)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
    #-----------馬名を取得

        for i in range(1,17):  #最大16頭分のデータの処理を行う
            # この変数が馬ごとのcssセレクタになる
            Horse_name_css = "#All_Result_Table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(4) > span > a"

            # ----Beautifulsoup--url
            link = soup.select(Horse_name_css)  # BeautifulSoupでセレクタからリンク取得
            for a in link:  # 1行ずつforを回す
                One_HorseData_url = a.attrs['href']  # リンクを取得(a.attrs['href]は構文のようなもの??)
            #URLがリストに含まれているときは処理しない
            if str(One_HorseData_url) in Horse_URL_MATCH:
                print(CountHorseNum,"レース目",i,"頭目です",'すでに取得済みです', One_HorseData_url)
                pass
            else:
                Horse_URL_MATCH.append(One_HorseData_url)  # リストにリンクを追加
                print(CountHorseNum,"レース目",i,"頭目です",One_HorseData_url) #週目=レース目
                time.sleep(1)
                Get_Data(One_HorseData_url)
    print("取得が終了しました")
    #--------------馬データを取得2



