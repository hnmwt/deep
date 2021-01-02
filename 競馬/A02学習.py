from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostClassifier


def L_DATA():
    import  csv
    import os

    DirPath = "output"  # 対象ディレクトリのパス
    Files_name = os.listdir(DirPath)  # output内のファイルリスト化
    count = len(Files_name)  # forの回数(output内のfileの数だけ)


    # START---------------データの読み込み処理-----------------------------

    Get_Data = []  # 機械学習用の配列
    for No in range(count):                     # 1頭ずつ機械学習させていく
        print(No + 1,"頭目")
        File = DirPath + "/" + Files_name[No]
        f = open(File, mode="r", encoding="utf-8")
        reader = csv.reader(f)  #与えられたファイル内の行を反復処理するような reader オブジェクトを返す
        i = 0                   #カウンター
        for row in reader:      #オブジェクトを1行ずつforで回す
                #print(row)
            if i == 0:
                i += 1
            else:
                Get_Data.append(row)    #dataに追加
        f.close()
        #print(Get_Data)
        print("Get_Dataに書き込みました")

        #END---------------データの読み込み処理-----------------------------

         #START-------------データ、ラベルの作成---------------------------------

        data = []
        label :int  = []

        for row in Get_Data:
             Weather = row[2]
             Round = row[3]
             Tousuu = row[4]
             Wakuban = row[5]
             Umaban = row[6]
             odds = float(row[7])
             Ninki = row[8]
             Tyakujun = row[9]
             Sekiryo = row[10]
             Field = row[11]
             Kyori = row[12]
             Umaba = row[13]
             Umabashisuu = row[14]
             Time = row[15]
             Tyakusa = row[16]
             Timeshisuu = row[17]
             Tsuuka = row[18]
             Race_Pace = float(row[19])
             Nobori = float(row[20])
             Umataijuu = row[21]
             Money = row[22]

#----------特徴量の整形---------------------------
             Weather = str(Weather)
             Round = str(Round)
             Tousuu = int(Tousuu)
             Wakuban = int(Wakuban)
             # Umaban,
             odds = float(odds)
             Ninki = int(Ninki)
             Tyakujun = int(Tyakujun)
             Sekiryo = int(Sekiryo)
             Field, = str(Field)
             Kyori = str(Kyori)
             Umaba = str(Umaba)
             Umabashisuu = int(Umabashisuu)
             Time = float(Time)
             Tyakusa = float(Tyakusa)
             Timeshisuu = int(Timeshisuu)
             # Tsuuka,
             Race_Pace = float(Race_Pace)
             Nobori = float(Nobori)
             Umataijuu = int(Umataijuu)
             Money = int(Money)
             # ----------特徴量の整形---------------------------

             append_data = [
                            Weather,
                            Round,
                            Tousuu,
                            Wakuban,
                            #Umaban,
                            odds,
                            Ninki,
                            Tyakujun,
                            Sekiryo,
                            Field,
                            Kyori,
                            Umaba,
                            Umabashisuu,
                            Time,
                            Tyakusa,
                            Timeshisuu,
                            #Tsuuka,
                            Race_Pace,
                            Nobori,
                            Umataijuu,
                            Money
                            ]

             data.append(append_data)
             label.append(Tyakujun)
        print("data:{}".format(data))
        print("label:{}".format(label))
        print("ラベル、データ作成完了")

# END-------------データ、ラベルの作成---------------------------------
        勾配ブースティング(data,label)
        線形回帰(data, label)
        data.clear()
        label.clear()
        append_data.clear()
        Get_Data.clear()

def 勾配ブースティング(data,label):
    from sklearn.ensemble import GradientBoostingClassifier
    X_train, X_test, y_train, y_test = train_test_split(data,label,random_state=1)

    gbrt = GradientBoostingClassifier(random_state=1)
    gbrt.fit(X_train, y_train)  # fitで学習
    print("訓練時の点数",gbrt.score(X_train, y_train))
    print("テストに対する予測", gbrt.predict(X_test))
    print("テスト時の点数",gbrt.score(X_test, y_test))

def 線形回帰(data,label):
    X_train, X_test, y_train, y_test = train_test_split(data,label,random_state=1)
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression()
    lr.fit(X_train,y_train) #学習
    print(lr.coef_)
    print(lr.intercept_)
    print("訓練時の点数",lr.score(X_train, y_train))
    print("テストに対する予測", lr.predict(X_test))
    print("テスト時の点数",lr.score(X_test, y_test))



L_DATA()


