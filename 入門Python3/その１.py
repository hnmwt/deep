from 入門Python3 import P177, 第7章, 第8章, P158, 第10章
# from collections import defaultdict
# food_counter = defaultdict(int)
# for food in ['spam', 'spam', 'eggs', 'spam']:
#     food_counter += 1
#
# for food,count in food_counter.items():
#     print(food, count)


#  Counterによる要素数の計算
from collections import Counter
breakfast = ['spam', 'spam', 'eggs', 'spam']
breakfast_counter = Counter(breakfast)
print(breakfast_counter)

lunch = ['eggs', 'eggs', 'becon']
lunch_counter = Counter(lunch)
print(lunch_counter)
#カウンタの結合
print('合計',breakfast_counter + lunch_counter)
print('朝食-昼食',breakfast_counter - lunch_counter)
print('昼食-朝食',lunch_counter - breakfast_counter)
print('共通要素',lunch_counter & breakfast_counter)


# デック(deque)の使い方 回文
def palindrome(word):
    from collections import deque
    dq = deque(word)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
        return True

palindrome('racecar')
palindrome('a')

import itertools
#itertools
for item in itertools.chain([1, 2],['a', 'b']):
    print(item)

'''
#無限反復
for item in itertools.cycle([1, 2]):
    print(item)
'''

#クラスの作成
class Person():
    def __init__(self,name):
        self.name = name
        print('Personくらす', self.name)

hunter = Person('Elmer Fudd')
print('hunterくらす', hunter.name)

P158.継承()
P177.コンポジションから()
第7章.第7章()
第8章.第8章()
第10章.第10章()
第10章.第10章区切り()
