def 継承():
    print("\n\nここからは継承~です")

    # スーパークラスの作成
    class Car():
        def exclaim(self):
            print("I'm a car! ")

    # サブクラスの作成
    class Yugo(Car):
        def exclaim(self):
            print("I'm a Yugo!! Much like a Car, but more Yugo-ish.")

        # サブクラスにしかないメソッドを作成
        def need_a_push(self):
            print("A little help here")

    # それぞれのクラスからオブジェクトを作る
    give_me_a_car = Car()
    give_me_a_yugo = Yugo()
    # exclaimメソッドを呼び出す
    give_me_a_car.exclaim()
    give_me_a_yugo.exclaim()
    # サブクラスにしかないメソッドを呼び出せる
    give_me_a_yugo.need_a_push()

    class Person():
        def __init__(self, name):
            self.name = name

    class MDPerson(Person):
        def __init__(self, name):
            self.name = "Doctor" + name

    class JDPerson(Person):
        def __init__(self, name):
            self.name = name + ", Esquire"

    class EmailPerson(Person):
        def __init__(self, name, email):
            super().__init__(name)  # 親クラスのPerson.__init__()を呼び出す.Personの引数はnameのみ
            self.email = email

    bob = EmailPerson('Bob Frapples', 'bob@frapples.com')
    # name,emailの引数にアクセス
    print(bob.name)
    print(bob.email)

    # ゲッター、セッター
    class Duck():
        def __init__(self, input_name):
            self.hidden_name = input_name

        def get_name(self):
            print('inside the getter')
            return self.hidden_name

        def set_name(self, input_name):
            print('inside the setter')
            self.hidden_name = input_name

        name = property(get_name, set_name)  # nameの第一引数がget_name、第二引数がset_nameに変化する

    fowl = Duck('Howard')
    # ゲッター get⇒メンバ関数をつかってるから
    fowl.name
    # 代入でセッター set⇒代入してるから
    fowl.name = 'Duffy'

    class Circle():
        def __init__(self, radius):
            self.radius = radius
        #@property ゲッターメソッドの前につけるデコレータ
        @property
        def diameter(self):
            return 2 * self.radius

    #circleクラスの引数を設定
    c = Circle(5)
    print(c.diameter)

    """radius属性はいつでも書き換えられる。diameterプロパティは
    radiusの現在の値から計算される"""
    c.radius = 7
    print(c.diameter)

    """getter,setterの設定は
    ・property(get_name, set_name)
    ・@property
    を使った2種類がある"""

    print('ここからはポリモーフィズム')
    #ポリモーフィズム
    class Quote():                           #スーパークラスの作成
        def __init__(self, person, words):
            self.person = person
            self.words = words
        def who(self):
            return self.person
        def says(self):
            return self.words + '.'

    class QuestionQuote(Quote):                #サブクラスの作成
        def says(self):
            return self.words + '.'

    class ExclamationQuote(Quote):             #サブクラスの作成
        def says(self):
            return self.words + '.'

    #異なる3種類のsays()メソッドが3つのクラスのために違う動作を提供する
    hunter = Quote('Elmer Fudd', "I'm hunting webbits")
    print(hunter.who(), 'says:', hunter.says())
    hunted1 = QuestionQuote('Bugs Bunny', "What's up, doc")
    print(hunted1.who(), 'says:', hunted1.says())
    hunted2 = ExclamationQuote('Duffy Duck', "I'ts rabbit season")
    print(hunted2.who(), 'says:', hunted2.says())

    #python特有のポリモーフィズム
    print('ダックタイピング')

    class BabblingBrock():
        def who(self):
            return 'Brock'
        def says(self):
            return 'Babble'

    brock = BabblingBrock()
    print(brock.who(),'\n',brock.says())

    #whoとsaysメソッドを持ちさえすれば共通のインターフェイスをもつオブジェクトとして利用できる(BabblingBrockを利用できる)
    def who_says(obj):
        print(obj.who(), 'says', obj.says())

    who_says(hunter)
    who_says(hunted1)
    who_says(hunted2)
    who_says(brock)

