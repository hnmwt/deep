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
X_column = ['日付', 'ドル円', 'ポンド円', 'オシレーター買いドル円', 'オシレーター中立ドル円', 'オシレーター売りドル円',
       '移動平均買いドル円', '移動平均中立ドル円', '移動平均売りドル円', 'オシレーター買いポンド円', 'オシレーター中立ポンド円',
       'オシレーター売りポンド円', '移動平均買いポンド円', '移動平均中立ポンド円', '移動平均売りポンド円', 'S&P500指数',
       'S&P500指数変化率', '日経平均株価', '日経平均株価変化率', 'UK100INDEX', 'UK100INDEX変化率',
       '恐怖指数', '恐怖指数変化率']
bid_act_parametor = np.array([np.nan, np.nan])  # 売り注文するかしないかパラメータ
ask_act_parametor = np.array([np.nan, np.nan])  # 買い決済するかしないかパラメータ
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
    y = df['ドル円(15分後)']  # 目的変数
    print(df.shape)
    print('特徴量：',X)
    print('目的変数：',y)
    #usdjpy = df.at[count_epi, 'ドル円']
    #********為替エピソード******************
    return df, X, y

# 現在のusdjoy価格
def usd_jpy(count_epi):
    usdjpy = df.at[count_epi, 'ドル円']
    return usdjpy

# ソフトマックス関数
def softmax(para):  # ソフトマックス関数
    m = para.shape
    pi = np.zeros((m))
    exp_para = np.exp(para)
    pi = exp_para /np.nansum(exp_para)
    pi = np.nan_to_num(pi)
    return pi

# 方策に従って新規行動をランダムに取得
def get_new_act(pi):  # 方策に従って新規行動をランダムに取得
    return np.random.choice([not_act, bid_act])

# 方策に従って決済行動をランダムに取得
def get_settle_act(pi):  # 方策に従って決済行動をランダムに取得
    return np.random.choice([not_act, ask_act])

# 新規注文の行動　　注文(買い、売り)するか、しないか
def act_bid_new(money, usdjpy, bid_act_parametor):  # エピソード毎の行動　　注文(買い、売り)するか、しないか
    global possession_flag
    if possession_flag == False: # 所持フラグがFalseのとき
        random_act = get_new_act(bid_act_parametor)  # 行動

        if random_act == not_act:
            bid_acted_num = not_act
            return  str('新規注文：無し'), money, bid_acted_num

        elif random_act == bid_act:
            biding_money = usdjpy*unit / 25 # 消費金額
            money = money - biding_money  # 注文後の所持金 = 所持金　- 注文価格
            biding_money = round(biding_money, 3)  # 少数第３位まで表示
            money = round(money, 3)  # 少数第３位まで表示

            bid_val.append(usdjpy) # 取引価格
            bid_num.append(unit)  # 取引単位
            bid_costmoney.append(biding_money)  # 現在の所持金
            acted_flag = True  # 注文したとき新規注文行動フラグをTrueにする
            bid_acted_num = bid_act
            possession_flag = True  #注文した時は所持フラグをTrueにする
            return str('新規注文：売り'), money, bid_acted_num
    else:  # 売り注文リストに既に要素が入っているときは注文できる
        bid_acted_num = not_act
        return str('新規注文：保有有り'), money, bid_acted_num


# 売りポジションを保有している時の行動　決済(買い)するか、しないか)
def act_ask_settlement(money, usdjpy, ask_act_parametor):  # 売りポジションを保有している時の行動　決済(買い)するか、しないか)
    benefit = 0
    global possession_flag
    if possession_flag == True:  # 売り注文リストに要素が入っているとき

        # 売り注文リストに要素が入っている場合
        random_act = get_settle_act(ask_act_parametor)  # 行動を決定する

        if random_act == not_act:
            ask_acted_num = not_act
            return str('無し'), money, benefit, ask_acted_num

        if random_act == ask_act:  # 1/2で保有している中で1番目の要素を決済する
            diff = bid_val[0] - usdjpy  # 現在の価格と保有しているポジションの差額を求める
            benefit = diff * bid_num[0]  # 儲け = 差額 *保有数　
            benefit = round(benefit, 3)  # 少数第３位まで表示
            money = money + benefit + bid_costmoney[0] # 所持金額に反映
            del bid_val[0]
            del bid_num[0]
            del bid_costmoney[0]
            ask_acted_num = ask_act
            possession_flag = False  # 決済した時は所持フラグをFalseにする
            return str('買い'), money, benefit, ask_acted_num
    else:  # 売り注文リストに要素が入っていないときは決済できない
        ask_acted_num = not_act
        return str('保有無し'), money, benefit, ask_acted_num  # 売り注文リストに要素が入っていない

# この関数が起点になっている
def bid_ask_settlement(end_epi, count_epi, money, money_capi, ask_rewards):  # 1エピソード行う
    while end_epi:
            usdjpy = usd_jpy(count_epi)

            # 新規行動
            order_acted, money, bid_acted_num = act_bid_new(money, usdjpy, bid_act_parametor) # 新規の行動(買う、売る、何もしない)
            new_bid_acted.append(bid_acted_num)  # 新規行動をリストに追加

            # 決済行動
            settlement_ask_acted, money, ask_benefit, ask_acted_num = act_ask_settlement(money, usdjpy, ask_act_parametor)
            settle_ask_acted.append(ask_acted_num)
            ask_rewards.append(ask_benefit)  # 報酬をリストに追加

            # ポジションリスト更新
            if possession_flag == True:
                possession_list.append(1)  # 保有中のときはポジションリストに1を追加
            elif possession_flag == False:
                possession_list.append(0)  # 保有していないときはポジションリストに0を追加

            # break処理
            if ask_acted_num == ask_act:  # 買い決済の時終了する
                print('***1エピソード終了(売り⇒買い)***')
                end_epi = False

            for i in zip(ask_val, ask_num, ask_costmoney):  # 保有中のポジションの価格
                money_capi += usdjpy * int(i[1]) / reva
            for i in zip(bid_val, bid_num, bid_costmoney):  # 保有中のポジションの価格
                money_capi += usdjpy * int(i[1]) / reva
            money_capi += money  # 時価総額

            print(count_epi+1,'step目:新規注文', order_acted,'所持金:',str(money),'円\n',
                 '保有買い注文:\n',ask_val,'\n',ask_num,'\n',ask_costmoney,'\n',
                 '保有売り注文:\n',bid_val, '\n',bid_num,'\n',bid_costmoney)
            print(count_epi + 1, 'step目:売り注文に対する決済', settlement_ask_acted, '利益', ask_benefit, '決済後所持金:', str(money),
                  '円')
            print('手持ちの時価価額(現金+ポジション)：', money_capi,"""'総報酬：',reward,'\n'""")
            print('**********************END******************************')
            count_epi = count_epi + 1  # エピソードの最後にカウンタを増やす
            money_capi = 0  # 時価総額を初期化する
    return ask_benefit, count_epi  # return：報酬,




df, X, y = data_shape()  # データ整形

iteration = 10  # 1イテレーションは10エピソード

bid_act_parametor = softmax(bid_act_parametor) # 売り注文するかしないかパラメータをソフトマックス化する
ask_act_parametor = softmax(ask_act_parametor) # 買い決済するかしないかパラメータをソフトマックス化する

for i in range(iteration):  # iイテレーション
    ask_benefit, count_epi = bid_ask_settlement(end_epi, count_epi, money, money_capi, ask_rewards)  # 1エピソード行う
print('ask_rewards 報酬：',ask_rewards)
print('new_bid_acted 新規行動：',new_bid_acted)
print('settle_ask_acted 決済行動：',settle_ask_acted)
print('possession_list：',possession_list)
X_train = X[:count_epi]


#*************ニューラルネットワーク作成*********
n_inputs = len(X_column)  # 入力数
model = keras.models.Sequential([
    keras.layers.Dense(10, activation='relu', input_shape=[n_inputs]),  # n_inputsを入力して隠れユニットを5つ出す
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid'),  # 選択は2択
])
optimizer = keras.optimizers.Adam(lr=0.01)  # オプティマイザ
loss_fn = keras.losses.binary_crossentropy  #  損失関数
#*************ニューラルネットワーク作成*********

model.compile(loss=loss_fn, optimizer=optimizer, metrics=['acc'])

# 学習
#history = model.fit()

def parametor_update(parametor, pi, acted):  # acted=新規、決済の行動数
    eta = 0.1  # 学習係数
    [s_count, a_count] = parametor.shape  # shapeで行列を算出
    total = len(acted)

    # パラメーターの変化量の計算
    delta_theta = parametor.copy()
    for i in range(0, s_count):
        for j in range(0, a_count):
            if not(np.isnan(para[0,j])):
                # ある状態である行動をとる回数
                sa_ij = [sa for sa in acted if sa == [i, j]]
                n_ij = len(sa_ij)

                # ある状態で何らかの行動をとる回数
                sa_i = [sa for sa in acted if sa[0] == i]
                n_i = len(sa_i)

                # パラメーターの変化量
                delta_theta [i, j] = (n_ij - pi[i, j] * n_i) / total
    # パラメーターの更新
    return parametor + eta * delta_theta