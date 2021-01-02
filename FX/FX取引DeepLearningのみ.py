import random
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import time

money : float = 500000 # 所持金
unit = 10000  # 取引通貨単位(暫定)
ask_val = []  # 取引通貨価格
ask_num = []  # 取引通貨単位
ask_costmoney = []  # 支払い金額
ask_money = [ask_val ,ask_num, ask_costmoney]  # 所持している買い通貨(構造体)
bid_val = []  # 取引通貨価格
bid_num = []  # 取引通貨単位
bid_costmoney = []  # 支払い金額
bid_money = [bid_val ,bid_num, bid_costmoney]  # 所持している売り通貨(構造体)
money_capi = 0  # 保有中のポジションの金額
reva = 25  # レバレッジ
max_epi = 200  # エピソードのMAX
ask_rewards = []  # エピソード毎の報酬リスト
bid_rewards = []  # エピソード毎の報酬リスト
ask_grads = []
bid_grads = []
not_act = 0  # 何もしない
ask_act = 1  # 買い
bid_act = 2  # 売り
act_order_type = [not_act, ask_act, bid_act]  # 注文時
act_settlement_bid_type = [not_act, bid_act]  # 買い注文決済時
act_settlement_ask_type = [not_act, ask_act]  # 売り注文決済時
end_epi = True  # エピソード終了フラグ
count_epi = 0  # エピソードカウンター
X_column = [ 'ドル円', 'ポンド円', 'オシレーター買いドル円', 'オシレーター中立ドル円', 'オシレーター売りドル円',
       '移動平均買いドル円', '移動平均中立ドル円', '移動平均売りドル円', 'オシレーター買いポンド円', 'オシレーター中立ポンド円',
       'オシレーター売りポンド円', '移動平均買いポンド円', '移動平均中立ポンド円', '移動平均売りポンド円', 'S&P500指数',
       'S&P500指数変化率', '日経平均株価', '日経平均株価変化率', 'UK100INDEX', 'UK100INDEX変化率',
       '恐怖指数', '恐怖指数変化率']

bid_act_parametor = np.array([np.nan, np.nan])  # 売り注文するかしないかパラメータ
ask_act_parametor = np.array([np.nan, np.nan])  # 買い決済するかしないかパラメータ

#act_parametor = np.array([np.nan, np.nan],  # 上記2個のパラメータを一つにしてみた
#                         [np.nan, np.nan])

#bid_act_parametor = softmax(bid_act_parametor)  # 売り注文パラメーター
#sk_act_parametor = softmax(ask_act_parametor)  # 買い決済パラメーター
new_bid_acted = []
settle_ask_acted = []
possession_flag = False
possession_list = []
# csvデータ整形
def data_shape():
    #------------csvからゴミデータを削除---------------------------
    df= pd.read_csv("為替情報.csv",encoding='shift_jis',index_col=0)
    #条件にマッチしたIndexを取得
    drop_index = df.index[df['ドル円(15分後)'] == 0]
    #条件にマッチしたIndexを削除
    df = df.drop(drop_index)
    df = df.dropna()  # NaNを削除
    df.to_csv('FX再現用pd自動整形.csv', encoding='shift_jis')
    #------------csvからゴミデータを削除---------------------------
    df= pd.read_csv("FX再現用pd自動整形.csv",encoding='shift_jis')
    print(df)
    X = df[X_column]  # 特徴量
    y_usdjpy_train = df['ドル円(15分後)']  # 目的変数
    y_gbpjpy_train = df['ポンド円(15分後)']  # 目的変数
    return df, X, y_usdjpy_train, y_gbpjpy_train







df, X, y_usdjpy_train, y_gbpjpy_train = data_shape()  # データ整形
X_train = X
print(df.dtypes)
# ニュートラルネットワーク作成
n_inputs = len(X_column)  # 入力数
model = keras.models.Sequential([
    keras.layers.Dense(10, activation='relu', input_shape=[n_inputs]),  # n_inputsを入力して隠れユニットを5つ出す
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(2, activation='sigmoid'),  # 選択は2択
])
optimizer = keras.optimizers.Adam(lr=0.01)  # オプティマイザ
loss_fn = keras.losses.binary_crossentropy  # 損失関数
model.compile(loss=loss_fn, optimizer=optimizer, metrics=['acc'])  # コンパイル

print(X_train.shape)
print(y_usdjpy_train.shape)

# 予測
history = model.fit(X_train, y_usdjpy_train, epochs=100, validation_split=0.1)

