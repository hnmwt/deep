import random
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras

usdjpy = []
gbpjpy = []
USDJPY_TECHNICALS_OCI_ASK = []
USDJPY_TECHNICALS_OCI_NEUTRAL = []
USDJPY_TECHNICALS_OCI_BID = []
all_csv_list = []
part_all_csv_list = []  # csvから指定したカラムを抜き出してリスト化
one_bid_reward = []
one_ask_reward = []


#------------csvからゴミデータを削除---------------------------
df= pd.read_csv("為替情報.csv",encoding='shift_jis',index_col=0)
#条件にマッチしたIndexを取得
drop_index = df.index[df['ドル円(15分後)'] == 0]
#条件にマッチしたIndexを削除
df = df.drop(drop_index)

df = df.dropna()  # NaNを削除

df.to_csv('FX再現用pd自動整形.csv', encoding='shift_jis')
#------------csvからゴミデータを削除---------------------------

with open('FX再現用pd自動整形.csv', mode='r',encoding='shift_jis') as f:
    header_flag = False
    for row in f:  # 1行ずつ読込み
        rows = row.rstrip().rsplit(',')
        if header_flag == True:  # 1行目はヘッダーのためpass
            usdjpy.append(rows[1])
            gbpjpy.append(rows[2])
            USDJPY_TECHNICALS_OCI_ASK.append(rows[3])
            USDJPY_TECHNICALS_OCI_NEUTRAL.append(rows[4])
            USDJPY_TECHNICALS_OCI_BID.append(rows[5])
            all_csv_list.append(rows)
            part_all_csv_list.append([rows[1],rows[3],rows[4],rows[5]])

        header_flag = True
    print('usdjpy要素数',len(usdjpy))
    print('gbpjpy要素数',len(gbpjpy))

print(part_all_csv_list)
#********為替エピソード******************
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
count_epi = 0  # エピソードカウンター
max_epi = 200  # エピソードのMAX
ask_reward = []  # 報酬
bid_reward = []# 報酬
ask_grads = []
bid_grads = []

not_act = 0  # 何もしない
ask_act = 1  # 買い
bid_act = 2  # 売り
act_order_type = [not_act, ask_act, bid_act]  # 注文時
act_settlement_bid_type = [not_act, bid_act]  # 買い注文決済時
act_settlement_ask_type = [not_act, ask_act]  # 売り注文決済時




def act(money):  # エピソード毎の行動　　注文(買い、売り)するか、しないか
    random_act = random.choice(act_order_type)  # 行動

    if random_act == not_act:
        return  str('無し'), money

    elif random_act == ask_act:
        asking_money = float(usdjpy[count_epi])*unit / 25  # 消費金額
        money = float(money) - asking_money  # 注文後の所持金 = 所持金　- 注文価格
        asking_money = round(asking_money, 3)  # 少数第３位まで表示
        money = round(money, 3)  # 少数第３位まで表示
        ask_val.append(float(usdjpy[count_epi]))
        ask_num.append(unit)
        ask_costmoney.append(asking_money)
        return str('買い'), money

    elif random_act == bid_act:
        biding_money = float(usdjpy[count_epi])*unit / 25 # 消費金額
        money = money - biding_money  # 注文後の所持金 = 所持金　- 注文価格
        biding_money = round(biding_money, 3)  # 少数第３位まで表示
        money = round(money, 3)  # 少数第３位まで表示

        bid_val.append(float(usdjpy[count_epi]))
        bid_num.append(unit)
        bid_costmoney.append(biding_money)
        return str('売り'), money


def bid_settlement(money,reward):  # 買いポジションを保有している時の行動　決済(売り)するか、しないか)
    benefit = 0
    if ask_val:  # 買い注文リストに要素が入っているとき
        random_act = random.choice(act_settlement_bid_type)

        if random_act == not_act:  # 何もしない
            bid_asked_num = 1
            return str('無し'), money, benefit, bid_reward, bid_asked_num

        if random_act == bid_act:  # 保有している中で1番目の要素を決済する
            diff = ask_val[0] - float(usdjpy[count_epi])  # 現在の価格と保有しているポジションの差額を求める
            benefit = diff * ask_num[0]  # 儲け = 差額 *保有数　
            benefit = round(benefit, 3)  # 少数第３位まで表示
            money = money + benefit + ask_costmoney[0]  # 所持金額に反映
            bid_reward.append(benefit)  # 報酬
            del ask_val[0]
            del ask_num[0]
            del ask_costmoney[0]
            bid_asked_num = 9
            return str('売り'), money, benefit, bid_reward, bid_asked_num
    bid_asked_num = 0
    return str('保有無し'), money, benefit, bid_reward, bid_asked_num


def ask_settlement(money,reward):  # 売りポジションを保有している時の行動　決済(買い)するか、しないか)
    benefit = 0
    if bid_val:  # 売り注文リストに要素が入っているか

        # 売り注文リストに要素が入っている場合
        random_act = random.choice(act_settlement_ask_type)

        if random_act == not_act:  # 1/2で何もしない
            ask_acted_num = 1
            ask_reward.append(0)  # 報酬
            return str('無し'), money, benefit, ask_reward, ask_acted_num

        if random_act == ask_act:  # 1/2で保有している中で1番目の要素を決済する
            diff = bid_val[0] - float(usdjpy[count_epi])  # 現在の価格と保有しているポジションの差額を求める
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

#*************ニューラルネットワーク作成*********
n_inputs = 4
model = keras.models.Sequential([
    keras.layers.Dense(5, activation='elu', input_shape=[n_inputs]),
    keras.layers.Dense(3, activation='softmax'),
])
optimizer = keras.optimizers.Adam(lr=0.01)
loss_fn = keras.losses.binary_crossentropy
#*************ニューラルネットワーク作成*********

def one_episode(): #売買を１エピソードだけ行う
    for episode in range(1):
        with tf.GradientTape() as tape:
            now_usdjpy = float(usdjpy[count_epi])
            #np_now_usdjpy = np.array(now_usdjpy)
            np_now_usdjpy = np.array(part_all_csv_list[count_epi], dtype=np.float32)
            print(part_all_csv_list[count_epi])
            print(np_now_usdjpy)
            print(np_now_usdjpy.dtype)
            #  買い注文に対する決済
            settlement_bid_acted, money, bid_benefit, bid_reward, bid_acted_num= bid_settlement(money,bid_reward) #
            print(count_epi+1,'回目:買い注文に対する決済', settlement_bid_acted, '利益',bid_benefit ,'決済後所持金:',str(money),'円')
            one_bid_reward.append(bid_benefit)  # 報酬を追加



            #  売り注文に対する決済
            #loss = tf.reduce_mean(loss_fn())
            settlement_ask_acted, money, ask_benefit, ask_reward, ask_acted_num = ask_settlement(money,ask_reward)
            print(count_epi+1,'回目:売り注文に対する決済', settlement_ask_acted,'利益', ask_benefit ,'決済後所持金:',str(money),'円')
            one_ask_reward.append(ask_benefit)  # 報酬を追加
            if ask_acted_num == 9:
                print('1エピソード終了(売り⇒買い)')
            #::::勾配:::::::::
            ask_proba = model(np_now_usdjpy[np.newaxis])  # NNを使い隠れ層を作成
            #print(ask_proba)
            #ask_action = (tf.random.uniform([1, 1]) > ask_proba)
            #print('ask_action:',ask_action)
            ask_target = tf.constant([[1. ]]) - tf.cast(ask_proba, tf.float32)
            #print('ask_target:', ask_target)
            ask_loss = tf.reduce_mean(loss_fn(ask_target, ask_proba))  # 損失を計算、ask_acted_num=実際に取った行動
            #print('ask_loss:',ask_loss)
            ask_grads = tape.gradient(ask_loss, model.trainable_variables)
            #print('ask_grads:',ask_grads)
            order_acted, money = act(money) # 新規の行動(買う、売る、何もしない)
            #::::勾配:::::::::

            for i in zip(ask_val, ask_num, ask_costmoney): # 保有中のポジションの価格
                money_capi += float(usdjpy[count_epi]) * int(i[1]) / reva
            for i in zip(bid_val, bid_num, bid_costmoney):  # 保有中のポジションの価格
                money_capi += float(usdjpy[count_epi]) * int(i[1]) / reva
            money_capi += money #時価総額



            print(count_epi+1,'回目:注文', order_acted,'所持金:',str(money),'円\n',
                 '買い注文:\n',ask_val,'\n',ask_num,'\n',ask_costmoney,'\n',
                 '売り注文:\n',bid_val, '\n',bid_num,'\n',bid_costmoney)
            print('手持ちの時価価額(現金+ポジション)：', money_capi,"""'総報酬：',reward,'\n'""")

            count_epi = count_epi + 1  # エピソードの最後にカウンタを増やす
            money_capi = 0

    #-----入力層-----
    #時価総額
    #総報酬
    #為替価格

def discount_rewards(rewards, discount_rate):  # 累積報酬を計算する
    discounted = np.array(rewards)
    for step in range(len(rewards) - 2, -1, -1):
        discounted[step] += discounted[step + 1] * discount_rate
    return discounted

def discount_and_normalize_rewards(all_rewards, discount_rate):  # 累積報酬を正規化する
    all_discounted_rewards = [discount_rewards(ask_reward, discount_rate)
                              for rewards in all_rewards]
    flat_rewards = np.concatenate(all_discounted_rewards)
    reward_mean = flat_rewards.mean()
    reward_std = flat_rewards.std()
    return [(discounted_rewards - reward_mean) / reward_std
            for discounted_rewards in all_discounted_rewards]


n_iterations = max_epi
n_episodes_per_update = 10
n_max_steps = 200
discount_factor = 0.95


optimizer = keras.optimizers.Adam(lr=0.01)
loss_fn = keras.losses.binary_crossentropy












for all_iteration_index in range(max_epi): # 1イテレーションをmax_epi回繰り返す
    for one_iteration_index in range(9):  # 1イテレーション = range回のエピソード


        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓def化しないでそのままいれる↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        with tf.GradientTape() as tape:
            now_usdjpy = float(usdjpy[count_epi])
            #np_now_usdjpy = np.array(now_usdjpy)
            np_now_usdjpy = np.array(part_all_csv_list[count_epi], dtype=np.float32)
            print(part_all_csv_list[count_epi])
            print(np_now_usdjpy)
            print(np_now_usdjpy.dtype)
            #  買い注文に対する決済
            settlement_bid_acted, money, bid_benefit, bid_reward, bid_acted_num= bid_settlement(money,bid_reward) #
            print(count_epi+1,'step目:買い注文に対する決済', settlement_bid_acted, '利益',bid_benefit ,'決済後所持金:',str(money),'円')
            #one_bid_reward.append(bid_benefit)  # 報酬を追加


            #  売り注文に対する決済
            #loss = tf.reduce_mean(loss_fn())
            settlement_ask_acted, money, ask_benefit, ask_reward, ask_acted_num = ask_settlement(money,ask_reward)
            print(count_epi+1,'step目:売り注文に対する決済', settlement_ask_acted,'利益', ask_benefit ,'決済後所持金:',str(money),'円')
            if ask_acted_num == 9:
                print('***1エピソード終了(売り⇒買い)***')
            #one_ask_reward.append(ask_benefit)  # 報酬を追加
            #::::勾配:::::::::
            ask_proba = model(np_now_usdjpy[np.newaxis])  # NNを使い隠れ層を作成
            #print(ask_proba)
            #ask_action = (tf.random.uniform([1, 1]) > ask_proba)
            #print('ask_action:',ask_action)
            ask_target = tf.constant([[1. ]]) - tf.cast(ask_proba, tf.float32)
            #print('ask_target:', ask_target)
            ask_loss = tf.reduce_mean(loss_fn(ask_target, ask_proba))  # 損失を計算、ask_acted_num=実際に取った行動
            #print('ask_loss:',ask_loss)
            ask_grads = tape.gradient(ask_loss, model.trainable_variables)  # 勾配
            #print('ask_grads:',ask_grads)
            #::::勾配:::::::::

            order_acted, money = act(money) # 新規の行動(買う、売る、何もしない)

            for i in zip(ask_val, ask_num, ask_costmoney): # 保有中のポジションの価格
                money_capi += float(usdjpy[count_epi]) * int(i[1]) / reva
            for i in zip(bid_val, bid_num, bid_costmoney):  # 保有中のポジションの価格
                money_capi += float(usdjpy[count_epi]) * int(i[1]) / reva
            money_capi += money #時価総額

            print(count_epi+1,'step目:新規注文', order_acted,'所持金:',str(money),'円\n',
                 '買い注文:\n',ask_val,'\n',ask_num,'\n',ask_costmoney,'\n',
                 '売り注文:\n',bid_val, '\n',bid_num,'\n',bid_costmoney)
            print('手持ちの時価価額(現金+ポジション)：', money_capi,"""'総報酬：',reward,'\n'""")

            count_epi = count_epi + 1  # エピソードの最後にカウンタを増やす
            money_capi = 0
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑def化しないでそのままいれる↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        # ask_grads = 勾配
        # ask_reward = 報酬
    print('ask_reward', ask_reward)
    # エピソードがrange回終了したら報酬を割り引き、正規化する：y = discounted
    ask_discounted = np.array(ask_reward)
    for i in range(9):
        ask_discounted[i] = ask_discounted[i] * (discount_factor ** (i+1))
    print('ask_discounted',ask_discounted)
    flat_ask_rewards = np.concatenate(ask_discounted)
    ask_reward_mean = flat_ask_rewards.mean()  # 平均
    ask_reward_std = flat_ask_rewards.std()  # 標準偏差
    for ask_discounted_one in ask_discounted:
        all_final_ask_rewards = ask_discounted - ask_reward_mean / ask_reward_std
    print('all_final_ask_rewards',all_final_ask_rewards)



    all_mean_ask_grads = []
    for var_index in range(len(model.trainable_variables)):
        mean_ask_grads = tf.reduce_mean(ask_reward * ask_grads[episode_index][var_index]
            for episode_index, final_ask_rewards in enumerate(all_final_ask_rewards))
        all_mean_ask_grads.append(mean_ask_grads)
    optimizer.apply_gradients(zip(all_mean_ask_grads, model.trainable_variables))
