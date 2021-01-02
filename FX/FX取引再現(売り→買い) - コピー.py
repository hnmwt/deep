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
ask_reward = []  # 報酬
ask_rewards = []  # エピソード毎の報酬リスト
bid_reward = []# 報酬
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
    X = df[['日付','恐怖指数変化率']]  # 特徴量
    y = df['ドル円(15分後)']  # 目的変数
    print(df.shape)
    print('特徴量：',X)
    print('目的変数：',y)
    #usdjpy = df.at[count_epi, 'ドル円']
    #********為替エピソード******************
    return df, X, y

def act_new_bid(money, usdjpy, acted_flag):  # エピソード毎の行動　　注文(買い、売り)するか、しないか
    random_act = random.choice(act_order_type)  # 行動

    if random_act == not_act or random_act == ask_act:
        return  str('新規注文：無し'), money, acted_flag

    elif random_act == bid_act:
        biding_money = usdjpy*unit / 25 # 消費金額
        money = money - biding_money  # 注文後の所持金 = 所持金　- 注文価格
        biding_money = round(biding_money, 3)  # 少数第３位まで表示
        money = round(money, 3)  # 少数第３位まで表示

        bid_val.append(usdjpy) # 取引価格
        bid_num.append(unit)  # 取引単位
        bid_costmoney.append(biding_money)  # 現在の所持金
        acted_flag = True  # 注文したとき新規注文行動フラグをTrueにする
        return str('新規注文：売り'), money, acted_flag

def ask_settlement(money,reward, usdjpy):  # 売りポジションを保有している時の行動　決済(買い)するか、しないか)
    benefit = 0
    if bid_val:  # 売り注文リストに要素が入っているか

        # 売り注文リストに要素が入っている場合
        random_act = random.choice(act_settlement_ask_type)

        if random_act == not_act:  # 1/2で何もしない
            ask_acted_num = 1
            ask_reward.append(0)  # 報酬
            return str('無し'), money, benefit, ask_reward, ask_acted_num

        if random_act == ask_act:  # 1/2で保有している中で1番目の要素を決済する
            diff = bid_val[0] - usdjpy  # 現在の価格と保有しているポジションの差額を求める
            benefit = diff * bid_num[0]  # 儲け = 差額 *保有数　
            benefit = round(benefit, 3)  # 少数第３位まで表示
            money = money + benefit + bid_costmoney[0] # 所持金額に反映
            ask_reward.append(benefit)  # 報酬
            del bid_val[0]
            del bid_num[0]
            del bid_costmoney[0]
            ask_acted_num = 9
            return str('買い'), money, benefit, ask_reward, ask_acted_num

    ask_acted_num = 0
    ask_reward.append(0)  # 報酬
    return str('保有無し'), money, benefit, ask_reward, ask_acted_num  # 売り注文リストに要素が入っていない

def bid_ask_settlement(end_epi, count_epi, money, ask_reward, money_capi):  # 1エピソード行う
    acted_flag = False  # 新規注文行動フラグ
    while end_epi:
            usdjpy = df.at[count_epi, 'ドル円']

            settlement_ask_acted, money, ask_benefit, ask_reward, ask_acted_num = ask_settlement(money, ask_reward, usdjpy)
            print(count_epi+1,'step目:売り注文に対する決済', settlement_ask_acted,'利益', ask_benefit ,'決済後所持金:',str(money),'円')
            if ask_acted_num == 9:  # 買い決済の時終了する
                print('***1エピソード終了(売り⇒買い)***')
                end_epi = False

            if acted_flag == False:  # 新規注文行動フラグがFalseの時新規決済行動を行う
                order_acted, money, acted_flag = act_new_bid(money, usdjpy, acted_flag) # 新規の行動(買う、売る、何もしない)

            for i in zip(ask_val, ask_num, ask_costmoney):  # 保有中のポジションの価格
                money_capi += usdjpy * int(i[1]) / reva
            for i in zip(bid_val, bid_num, bid_costmoney):  # 保有中のポジションの価格
                money_capi += usdjpy * int(i[1]) / reva
            money_capi += money  # 時価総額

            print(count_epi+1,'step目:新規注文', order_acted,'所持金:',str(money),'円\n',
                 '買い注文:\n',ask_val,'\n',ask_num,'\n',ask_costmoney,'\n',
                 '売り注文:\n',bid_val, '\n',bid_num,'\n',bid_costmoney)
            print('手持ちの時価価額(現金+ポジション)：', money_capi,"""'総報酬：',reward,'\n'""")

            count_epi = count_epi + 1  # エピソードの最後にカウンタを増やす
            money_capi = 0  # 時価総額を初期化する
    return ask_reward, count_epi  # return：報酬,


# データ整形
df, X, y = data_shape()
# 1エピソード行う


ask_reward, count_epi = bid_ask_settlement(end_epi, count_epi, money, ask_reward, money_capi)
ask_rewards.append(ask_reward)


#*************ニューラルネットワーク作成*********
n_inputs = 4  # 入力は4つ
model = keras.models.Sequential([
    keras.layers.Dense(5, activation='relu', input_shape=[n_inputs]),  # n_inputsを入力して隠れユニットを5つ出す
    keras.layers.Dense(1, activation='sigmoid'),  # 選択は2択
])
optimizer = keras.optimizers.Adam(lr=0.01)  # オプティマイザ
loss_fn = keras.losses.binary_crossentropy  #  損失関数
#*************ニューラルネットワーク作成*********




