"""キーボードから英語と算数の成績を入力し、入力された得点とともに、得点の合計と平均を計算して表示するプログラムを作成せよ。
実行結果
英語の成績を入力して下さい> 65
数学の成績を入力して下さい> 88
英語の得点: 65
数学の得点: 88
合　　　計: 153
平　　　均: 76.5"""
try:
    print("英語の成績を入力して下さい")
    english = int(input())
    print("数学の成績を入力して下さい")
    math = int(input())
except:
    print('数値で入力してください')

print("英語の得点:",english)
print("数学の得点:",math)

