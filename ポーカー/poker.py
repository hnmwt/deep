#import
import random

"""Trump_Spade = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Trump_Heart = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Trump_Diamond = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Trump_Club = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Trump_all = [Trump_Spade,       #絵柄ごとの2次元配列
             Trump_Heart,
             Trump_Diamond,
             Trump_Club]"""
Trump_all = []      #52枚のカード
def set_Trump():      #52枚のトランプを作成(前準備)
    for act in range(4):    #絵柄4種類
        if act == 0:
            mark = "Spade"
        elif act == 1:
            mark = "Heart"
        elif act == 2:
            mark = "Diamond"
        elif act == 3:
            mark = "Club"
        for num in range(13): #1-13までのカード
            Trump_all.append(str(num) + ',' + mark)


def Give_out_Card():
    for i in range(5):  # Trump_allの要素が存在している間ループ
        Get_Trump = random.choice(Trump_all)  # 絵柄をランダムに指定
        Player1.append(Get_Trump)  # ゲットしたトランプをプレイヤーの手札に追加
        Trump_all.remove(Get_Trump)  # ゲットしたカードをリストから削除

        Get_Trump = random.choice(Trump_all)  # 絵柄をランダムに指定
        Player2.append(Get_Trump)  # ゲットしたトランプをプレイヤーの手札に追加
        Trump_all.remove(Get_Trump)  # ゲットしたカードをリストから削除

#始まり
set_Trump()
print("2人で対戦")
#human_count = int(input())# 何人で対戦するか?後で考える

Player1 = []
Player2 = []

Give_out_Card()
print('あなたの手札です\n',Player1)




