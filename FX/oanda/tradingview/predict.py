import pandas as pd
import numpy as np
import datetime
from tensorflow import keras
import time
import pickle
import math
import backtest_variable
import param
backtest = backtest_variable.backtest
#get_csv_name = r".\FX_GBPJPY, 30.csv"
#get_csv_name = r".\OANDA_USDJPY, 5.csv"
get_csv_name = r".\OANDA_USDJPY, 15.csv"
train_data_name = r".\Intermediate\predict.py中間ファイル.csv"
pred_data_name = r".\Intermediate\predict.py予測ファイル.csv"

pred_close = 0
pred_high = 0
pred_low = 0


syukai_flag = False  # 周回フラグ

# 特徴量データを取得
def create_train_data(file_name, bktest_orbit):
    df = pd.read_csv(file_name, encoding='shift_jis')
    if backtest == True:
        df = df[:bktest_orbit]
    MACD_Cross = df['Cross'].copy()
    df.drop(labels='Cross', axis=1, inplace=True)  # MACDの追加のためNanの多いカラムを削除する 21.02.28
    df = df.dropna()
    df['time'] = pd.to_datetime(df['time']  )#, format='%Y-%m-%d-%A %H:%M:%S')  # 日付カラムを日付型に変換
    df['time(hour)'] = df['time'].dt.hour  # hourをデータに追加
    df['time(minute)'] = df['time'].dt.minute  # minuteをデータに追加
    df['time(weekday)'] = df['time'].dt.dayofweek  # minuteをデータに追加
    df.to_csv(train_data_name, index=False)
    MACD = df['MACD']
    MACD_signal = df['Signal Line']
    return df, MACD, MACD_signal, MACD_Cross


def format(num):
    num = "{:.3f}".format(float(num))  # 書式編集
    return num

def reading_model(model_dir, scalar_dir): # モデルと重みを読み込む関数
    model = keras.models.load_model(model_dir + '\model.hdf5')  # モデルを読込み
    model.load_weights(model_dir + '\param.hdf5')  # 重みを読込み
    X_train_save_scaler = pickle.load(open(scalar_dir + '\X_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    y_train_save_scaler = pickle.load(open(scalar_dir + '\y_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    return model, X_train_save_scaler, y_train_save_scaler

def create_df(df, column_start, X_train_save_scaler):  # df作成関数
    X_train_columns = len(df.columns) - 1  # 特徴量のカラム数を計算
    time = df.iloc[column_start, 0]        # 時間[行, 列]
    df = df.loc[:, 'open':'time(weekday)']  # [行 , 列名称(始まり):列名称(終わり)]
    #***21.03.30追加start
    df = df[-30: -1]  # dfの行数を30にする
    # ***21.03.30追加end
    df = X_train_save_scaler.transform(df)  # 正規化
    X_train = df.copy()                           # dfをコピー
    X_train = np.array(X_train).reshape(-1, X_train_columns, 1)  # 特徴量の形状(3次元)
    return X_train, time

def PRED(X_train, y_train_save_scalar, column_start, column_end, model):# 予測関数
    pred = model(X_train)  # 予測
    pred = y_train_save_scalar.inverse_transform(pred)  # 予測結果の正規化をデコード
    pred = pred[column_start:column_end]  # 対象の行を抜き出す
    pred = "{:.3f}".format(float(pred))  # 書式編集
    return pred

def create_PRED_time(time, pred, hour): # 予測日時作成関数
    after_time = time + datetime.timedelta(hours=hour+9+hour)  # 日本時間を計算、hour足のデータのため予測時刻= 現在時刻 + hour後
    after_time = "{0:%Y-%m-%d %H:%M}".format(after_time)
    pred_time = {str(after_time) : str(pred)}  # 時間、予測レートを辞書化
    return pred_time, after_time

# モデルデータから未来のレートを予測
def predict(model_dir, scalar_dir, df, hour, column_start, column_end):
    model, X_train_save_scaler, y_train_save_scaler = reading_model(model_dir, scalar_dir)  # モデル、重みを読み込む
    X_train, time = create_df(df, column_start, X_train_save_scaler)
    pred = PRED(X_train, y_train_save_scaler, column_start, column_end, model)
    pred_time, after_time = create_PRED_time(time, pred, hour)
    return pred_time, pred, after_time

# 予測間隔をhourに変換
def met_hour(next_time):
    next_time = 60 / next_time
    next_time = 100 / next_time
    next_time = next_time * 0.01
    return next_time

def MACD_sign(MACD, MACD_signal, MACD_Cross):
    BUY = 0
    SELL = 1
    NG = 9
    MACD_judge = NG
    Cross_judge = NG
    MACD_last_diff_flag = False

    MACD = MACD.values.tolist()

    MACD_last = MACD[-2]  # 最終の値
    MACD_last2 = MACD[-3]
    MACD_last3 = MACD[-4]
    MACD_Cross_last = MACD_Cross[-2:-1]

    MACD_last_diff = abs(MACD_last - MACD_last2)  # MACDの差額
    MACD_last_diff_threshold = 0.003              # MACDの差額の閾値

    if MACD_last_diff_threshold < MACD_last_diff:  # 差額が閾値以上
        MACD_last_diff_flag = True

    # MACDが0を超過しているとき
    if MACD_last > 0:
        if MACD_last > MACD_last2: #> MACD_last3 and MACD_last_diff_flag == True:  #
            MACD_judge = BUY
            # 保有しているsellポジションは決済
        elif MACD_last < MACD_last2: # < MACD_last3 and MACD_last_diff_flag == True :
            MACD_judge = SELL
            # 保有しているbuyポジションは決済
    # MACDが0未満のとき
    elif MACD_last < 0:
        if MACD_last < MACD_last2: # < MACD_last3 and MACD_last_diff_flag == True :
            MACD_judge = SELL
            # 保有しているbuyポジションは決済
        elif MACD_last > MACD_last2: # > MACD_last3 and MACD_last_diff_flag == True :
            MACD_judge = BUY
            # 保有しているsellポジションは決済

    # MACDのシグナルが出たとき
    if math.isnan(MACD_Cross_last):
        pass
    elif float(MACD_Cross_last) > 0: # 売りシグナル
        Cross_judge = SELL
    elif float(MACD_Cross_last) < 0: # 買いシグナル
        Cross_judge = BUY

    return MACD_judge, Cross_judge

# 予測関数
def summarize(df, syukai_flag, pred_close, pred_high, pred_low, next_time, backtest_col_st):
    backtest_col_ed = backtest_col_st + 1
    t = met_hour(next_time)
    # 2週目以降は前回の予測値を変数に格納  ※処理1/2
    if syukai_flag == True:
        last_pred_close = pred_close
        last_pred_high = pred_high
        last_pred_low = pred_low

    dict_pred_close, pred_close, pred_after_time = predict(r'.\model\USDJPY_15m_turning_close_production',
                                                                 r'dump\USDJPY_15m_dump_turning_close_production', df, t, -2, -1) # closeを予測
    dict_pred_high, pred_high, pred_after_time = predict(r'.\model\USDJPY_15m_turning_high_production',
                                                              r'dump\USDJPY_15m_dump_turning_high_production', df, t, -2, -1)  # highを予測
    dict_pred_low, pred_low, pred_after_time = predict(r'.\model\USDJPY_15m_turning_low_production',
                                                              r'dump\USDJPY_15m_dump_turning_low_production', df, t, -2, -1)  # lowを予測


    # 1週目に限り前回の予測も行う
    if syukai_flag == False:
      #  before_pred, before_pred_one30m, pred_after_time = read_model('.\model\GBPJPY_30m', df, 0.5, -3, -2)  # 0.5時間後の予測
        diff_close = 0  # 差額は初回は0固定
        diff_high = 0
        diff_low = 0

    # 2週目以降は前回の予測との差を求める
    elif syukai_flag == True:
        diff_close = float(pred_close) - float(last_pred_close)  # 前回との差を求める,close
        diff_close = format(diff_close)
        diff_high = float(pred_high) - float(last_pred_high)  # 前回との差を求める,high
        diff_high = format(diff_high)
        diff_low = float(pred_low) - float(last_pred_low)  # 前回との差を求める,low
        diff_low = format(diff_low)

    syukai_flag = True
    return syukai_flag, pred_close, diff_close, pred_high, diff_high, pred_low, diff_low, pred_after_time

#def VOLUME_judge(df, tp_point, sl_point):
#    volume = df.iat[]

# デバッグ用
if __name__ == '__main__':
    syukai_flag = False
    csv_time = 5
    model_dir = '.\model'
    scalar_dir = '.\dump'
    while True:
        df, MACD, MACD_signal, MACD_Cross = create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
        syukai_flag, pred, diff, pred_after_time = pred(df, syukai_flag,pred, csv_time, model_dir, scalar_dir)  # 値を予測
        MACD_judge, Cross_judge = MACD_sign(MACD, MACD_signal, MACD_Cross)
        print('完了')
        time.sleep(5)











