import pandas as pd
import numpy as np
import  csv
import datetime
CSV = '\Database_Horse_Race202001-10_Reformat.csv'
INPUT = "input_DataBase"
OUTPUT = "output_DataBase"
READINGINPUT_CSV = INPUT + CSV
WRITINGOUTPUT_CSV = OUTPUT + CSV

print(WRITINGOUTPUT_CSV)
df = pd.read_csv(READINGINPUT_CSV,engine='python',encoding='utf-8')
HEADER = list(df.columns.values)  # ヘッダーの要素を取得
print(HEADER)
for num in HEADER:
    print(num, df[str(num)].unique())  # データの値の内容を取得(整形するため)
#print(df)

df.drop("騎手", axis=1)


df = df.replace({'天気': {'晴': 0, '曇': 1, '雨': 2, '小雨': 3, '雪': 4, '小雪': 5}})
#df = df.loc[df['天気'] != 5, '天気'] = 10

#df = df.loc(df['天気'] != 0)
#df = df.loc(df['天気'] != 1)

print(df)
#df = pd.DataFrame.to_csv(self=df,path_or_buf="output_DataBase\Database_Horse_Race202001-10_Reformat.csv",sep=',',encoding="shift_jis")


#--------------forで回すタイプ------------------
with open(READINGINPUT_CSV, mode='r',encoding='utf-8') as rf:
    #header = next(reader)
    with open(WRITINGOUTPUT_CSV, mode='w', encoding='shift_jis') as wf:
        #read = rf.readlines()
        #print(read[0])
        #print(read[1])
        for row in rf:
            row = row.rstrip() .rsplit(',')
# --------------forで回すタイプ------------------

            Horse_name = row[0]
            Whattime = row[1]
            Weather = row[2]
            Round = row[3]
            Racename = row[4]
            Horse_Num = row[5]
            Wakuban = row[6]
            Horse_No = row[7]
            Odds = row[8]
            Fun = row[9]
            Result = row[10]
            Human = row[11]
            Kinryo = row[12]
            Field = row[13]
            Range = row[14]
            Ground = row[15]
            Ground_Index = row[16]
            Time = row[17]
            Difference = row[18]
            Time_Index = row[19]
            Passing = row[20]
            Pace = row[21]
            Up = row[22]
            Horse_Weight = row[23]
            Money = row[24]

            # ------------天気--------------
            if row[2] == '晴':
                row[2] = 0
            elif row[2] == '曇':
                row[2] = 1
            elif row[2] == '雨':
                row[2] = 2
            elif row[2] == '小雨':
                row[2] = 3
            elif row[2] == '小雪':
                row[2] = 4
            elif row[2] == '雪':
                row[2] = 5
            else:
                row[2] = 'NaN'
            # ------------天気--------------

            # ------------枠番--------------
            # if row[]
            # ------------枠番--------------
            # ------------フィールド--------------
            row[13] = row[13][0:1]
            if row[13] == 'ダ':
                row[13] = 0
            if row[13] == '芝':
                row[13] = 5
            if row[13] == '障':
                row[13] = 9
            else:
                row[13] = 'NaN'
            # ------------フィールド--------------

            # ------------距離--------------
            row[14] = row[14][1:5]
            # ------------距離--------------

            # ------------馬場--------------
            if row[15] == '良':
                row[15] = 0
            elif row[15] == '稍':
                row[15] = 1
            elif row[15] == '重':
                row[15] = 2
            elif row[15] == '不':
                row[15] = 3
            else:
                row[15] = 'NaN'
            # ------------馬場--------------

            # ------------馬場指数--------------
            row[16]

            # ------------馬場指数--------------

            # ------------タイム--------------
            try:
                row[17] = row[17].replace(':', '.')
                row[17] = row[17].rstrip().rsplit('.')
                minute = float(row[17][0]) * 60
                second = float(row[17][1])
                millisecond = float(row[17][2])
                row[17] = minute + second + millisecond
            except:
                row[17] = 'NaN'

            # ------------タイム--------------

            # ------------タイム指数--------------
            if row[19] is not int:
                row[19] = 'NaN'
            # ------------タイム指数--------------

            # ------------馬体重--------------
            row[23] = row[23][0:3]
            # ------------馬体重--------------

            # ------------賞金--------------
            try:
                row[24] = float(row[24])
                row[24] = row[24] * 10
            except:
                row[24] = 'NaN'
            # ------------賞金--------------

            # ------------削除--------------
            del row[20]
            del row[11]
            del row[6]


            # ------------削除--------------

            # writerow,書き込み(対象:f,改行方法:\n),
            writer = csv.writer(wf, lineterminator='\n',).writerow(row)
            # writerow,1行ずつ書き込み
    print('書き込みました')