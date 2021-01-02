
def Zizensakujo():  # 前回の残りファイルを削除

    import os
    import shutil
    if os.path.exists("output"):    #フォルダがあるとき
        shutil.rmtree("output")
    if not os.path.exists("output"): #フォルダがない時
        os.mkdir("output")
    if os.path.exists("input_parser"):    #フォルダがあるとき
        shutil.rmtree("input_parser")
    if not os.path.exists("input_parser"): #フォルダがない時
        os.mkdir("input_parser")

"""
def parser_Syutoku(url)では各馬のデータページのurlを取得する
"""

def Zentai_Syutoku(url,tousu):    # HTTPリクエストを送信してHTMLを取得します
    from bs4 import BeautifulSoup
    import requests

    response = requests.get(url)  # urlを指定
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')  # soupを使い抽出していく
    with open('zentai.text', mode='w', encoding='utf-8') as f:
        f.write(str(soup))
    print('htmlの書き込み完了')  # 必要ないが一応textに書き込み

    with open("input_parser/" + 'link.text', mode='w', encoding='utf-8') as f:
        for i in range(1, tousu + 1):  # 頭数だけfor文で回す
            selector = "#tr_" + str(i) + " > td.HorseInfo > div > div > span.HorseName >a[href]"
            # print(selector)
            horse_syousai = soup.select(selector)  # urlの階層情報を取得
            for a in horse_syousai:  # 1行ずつforを回す
                link = a.attrs['href']  # リンクを取得(a.attrs['href]は構文のようなもの??)
            f.write(link + '\n')
            print(i, '頭目', link)  # リンクをプリント




def Yomikomi():  # def Yomikomi()ではlink.text内のリンクを一行ずつ読み込む
    import time
    import requests
    from bs4 import BeautifulSoup
    # ------------------変数宣言------------------------------------
    link_list: str = []  # リストを確保
    i : int = 1  # txtファイル名称用のカウンター変数
    # --------------------------------------------------------

    with open("input_parser/" + 'link.text', mode='r', encoding='utf-8') as f:
        for row in f:  # 1行ずつforで回す
            row = row.rstrip()  # rstrip()は改行、タブ、スペースを削除する
            link_list.append(row)  # link_listにurlを格納
        # print(link_list)

    for url in link_list:  # 格納したリンク分forで回す
        print(i, "頭目処理中")
        Kobetsu_Header(i)
        response = requests.get(url)  # urlを指定
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')  # 1行ずつパーサーする
        name : str = "馬" + str(i)  # 出力ファイル名称
        with open("input_parser/" + name + ".text", mode='w', encoding='utf-8') as f:  # ファイルを開いて
            f.write(str(soup))  # 書き込み
        KobetsuDATA_syutoku(soup, i)  # 馬別のデータをパースする
        time.sleep(1)  # 1秒停止
        i += 1  # カウンターを+1する

    print('馬別情報書き込み完了')  # 必要ないが一応textに書き込み

def Kobetsu_Header(count):  # data.csvのヘッダー作成
    import csv

    Header = [
        "00馬名",
        "01開催場所",
        "02天気",
        "03ラウンド",
        #"04レース名",
        "05頭数",
        "06枠番",
        "07馬番",
        "08オッズ",
        "09人気",
        "10着順",
        #"11騎手",
        "12斤量",
        "13フィールド",
        "14距離",
        "15馬場",
        "16馬場指数",
        "17タイム",
        "18着差",
        "19タイム指数",
        "20通過",
        "21ペース",
        "22上り",
        "23馬体重",
        "24賞金",
        ]
    with open("output/data" + str(count) + ".csv", mode="a", encoding="utf-8") as f:
        # f.writerows(str(Header) + "\n")                    #ヘッダー書き込み
        writer = csv.writer(f, lineterminator='\n').writerow(Header)


def KobetsuDATA_syutoku(soup,count):  # 馬別のデータをパースして取得、データの取得、整形
    import csv

    import decimal
    for i in range(1, 5):        #過去4回分のデータを書き込む
    # 対象の階層を指定する
        d00_Uma_name = "#db_main_box > div.db_head.fc > div.db_head_name.fc > div.horse_title > h1"
        d01_Kaisaibasyo = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child("+str(1)+") > a"
        d02_Weather = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(3)"
        d03_Round = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(4)"
        #d04_Racename
        d05_Tousuu = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(7)"
        d06_Wakuban = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(8)"
        d07_Umaban = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(9)"
        d08_odds = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(10)"
        d09_Ninki = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(11)"
        d10_Chakujun = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(12)"
        #d11_human
        d12_Kinryo = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(14)"
        d13_14_Kyori = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(15)"
        d15_Umaba = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(16)"
        d16_Umabashisuu = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:index1.txt_right"
        d17_Time = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(18)"
        d18_Tyakusa = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(19)"
        d19_Timeshisuu = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:index2.txt_right"
        d20_Tsuuka = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(21)"
        d21_pace = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(22)"
        d22_Nobori = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(23)"
        d23_UmaTaijuu = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(24)"
        d24_Money = "#contents > div.db_main_race.fc > div > table > tbody > tr:nth-child("+str(i)+") > td:nth-child(28)"


        # 対象の階層から情報を抜き出す
        Get_Uma_name = soup.select_one(d00_Uma_name).string
        Get_Kaisaibasyo = soup.select_one(d01_Kaisaibasyo).string  # select はすべての要素をリストで返す
        Get_Weather = soup.select_one(d02_Weather).string  # select_one　は要素を1つだけ取り出す
        Get_Round = soup.select_one(d03_Round).string
        #Get_Racename
        Get_Tousuu = soup.select_one(d05_Tousuu).string
        Get_Wakuban = soup.select_one(d06_Wakuban).string
        Get_Umaban = soup.select_one(d07_Umaban).string
        Get_odds = soup.select_one(d08_odds).string
        Get_Ninki = soup.select_one(d09_Ninki).string
        Get_Chakujun = soup.select_one(d10_Chakujun).string
        #Get_human
        Get_Kinryo = soup.select_one(d12_Kinryo).string
        Get_Kyori = soup.select_one(d13_14_Kyori).string
        Get_Umaba = soup.select_one(d15_Umaba).string
        Get_Umabashisuu = soup.find_all(d16_Umabashisuu)
        Get_Time = soup.select_one(d17_Time).string
        Get_Tyakusa = soup.select_one(d18_Tyakusa).string
        Get_Timeshisuu = soup.find_all(d19_Timeshisuu)
        Get_Tsuuka = soup.select_one(d20_Tsuuka).string
        Get_pace = soup.select_one(d21_pace).string
        Get_Nobori = soup.select_one(d22_Nobori).string
        Get_UmaTaijuu = soup.select_one(d23_UmaTaijuu).string
        Get_Money = soup.select_one(d24_Money).string

        #-------------整形-----------------------------

        # Get_Kyoriからダート、距離を算出
        Get_Field = Get_Kyori[0:1]  # Get_Kyoriから1文字目をスライスしてフィールドを取得
        Get_Kyori = Get_Kyori[1:]  # Get_Kyoriから1文字目以降をスライスして距離を取得

        # Get_Timeを秒数に変換

        if Get_Time:
            Get_Time = Get_Time.replace(':', '.')
            Get_Time = Get_Time.rstrip().rsplit('.')
            minute = float(Get_Time[0]) * 60
            second = float(Get_Time[1])
            millisecond = float(Get_Time[2])
            Get_Time = minute + second + millisecond
        else:
            continue


        #ペースを2つの平均にする
        Get_pace = Get_pace.rstrip().rsplit('-')
        saisoku = decimal.Decimal(Get_pace[0])
        dousoku = decimal.Decimal(Get_pace[1])
        Get_pace = (saisoku + dousoku) / 2

        # Get_UmaTaijuuを3桁目まで表示する
        Get_UmaTaijuu = Get_UmaTaijuu[:3]

        #Get_moneyの少数
        #Get_Money = decimal.Decimal(Get_Money)
        #Get_Money = decimal.Decimal(Get_Money)


    # ラベルの作成
        # **********************************************************
        # 天気
        # 晴れ('晴') → 0
        # 曇り('曇') → 1
        # 小雨('小雨')   → 2
        # 雨('雨')   → 3
        # **********************************************************
        if Get_Weather == "晴":
            Get_Weather = "0"
        elif Get_Weather == "曇":
            Get_Weather = "1"
        elif Get_Weather == "小雨":
            Get_Weather = "2"
        elif Get_Weather == "雨":
            Get_Weather = "3"
        # **********************************************************
        # フィールド
        # ダート('ダ') → 0
        # 芝生('芝') → 1
        # 稍('稍') → 2
        # **********************************************************
        if Get_Field == "ダ":
            Get_Field = "0"
        elif Get_Field == "芝":
            Get_Field = "1"
        elif Get_Field == "稍'":
            Get_Field = "2"
        # **********************************************************
        # 馬場    状態
        # 良     → 0
        # 稍重     → 2
        # 重     → 3
        # 不     → 4
        # **********************************************************
        if Get_Umaba == "良":
            Get_Umaba = "0"
        elif Get_Umaba == "稍":
            Get_Umaba = "1"
        elif Get_Umaba == "稍重":
            Get_Umaba = "2"
        elif Get_Umaba == "重":
            Get_Umaba = "3"
        elif Get_Umaba == "不":
            Get_Umaba = "4"

        # **********************************************************
        # Money
        # 空文字    → 0
        #
        # **********************************************************
        if Get_Money != '':
            Get_Money = str(Get_Money)
            Get_Money = "0"



        Syuturyoku = [  # リストを作成
        Get_Uma_name,
        Get_Kaisaibasyo,
        Get_Weather,
        Get_Round,
        # Get_Racename,
        Get_Tousuu,
        Get_Wakuban,
        Get_Umaban,
        Get_odds,
        Get_Ninki,
        Get_Chakujun,
        # Get_human,
        Get_Kinryo,
        Get_Field,
        Get_Kyori,
        Get_Umaba,
        Get_Umabashisuu,
        Get_Time,
        Get_Tyakusa,
        Get_Timeshisuu,
        Get_Tsuuka,
        Get_pace,
        Get_Nobori,
        Get_UmaTaijuu,
        Get_Money
        ]
        with open("output/data" + str(count) + ".csv", mode="a", encoding="utf-8") as f:
            # f.writerows(str(Syuturyoku) + "\n")                    #データ書き込み
            writer = csv.writer(f, lineterminator='\n').writerow(Syuturyoku) #writerow,書き込み(対象:f,改行方法:\n),
                                                                            # writerow,1行ずつ書き込み








