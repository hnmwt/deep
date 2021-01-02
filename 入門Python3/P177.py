def コンポジションから():
    print('↓コンポジション')
    #コンポジション
    #bill = くちばし　tail = しっぽ
    class Bill():
        def __init__(self, description):
            self.description = description

    class Tail():
        def __init__(self, length):
            self.length = length

    class Duck():
        def __init__(self, bill, tail):
            self.bill = bill
            self.tail = tail
        def about(self):
            print('This duck has a', self.bill.description, 'bill and a',
                  self.tail.length, 'tail')

    tail = Tail('long')
    bill = Bill('wide orange')
    duck = Duck(bill, tail)
    duck.about()

    #名前付きタプル
    from collections import namedtuple
    Duck = namedtuple('Duck', 'bill tail')
    duck = Duck('wide orange', 'long')
    print(duck)                 #名前を指定しても呼び出せる
    print(duck.bill)
    print(duck.tail)
    #名前付きタプルは辞書からも作れる
    parts = {'bill': 'wide orange', 'tail': 'long'}
    duck2 = Duck(**parts)
    print(duck2)
    