def 第7章():
    print('\n↓Unicode文字列')

    #文字から名前を引き出し、名前から文字を引き出す関数を定義
    def unicode_test(value):
        import  unicodedata
        name = unicodedata.name(value)      #unicode文字を与えると大文字の名前を返す
        value2 = unicodedata.lookup(name)   #名前を与えるとunicode文字を返す
        print('value="%s", name="%s", value2="%s"'
                            % (value, name, value2))
    #文字を試してみる
    unicode_test('A')
    unicode_test('$')
    unicode_test('\u00a2')
    unicode_test('\u20ac')

    #snowmanという変数にUnicode文字列'\u2603'を代入
    snowman = '\u2603'
    #snowmanは1文字の　Python Unicode文字列である
    print(len(snowman))
    #Unicode文字をバイトシーケンスにエンコードする
    ds = snowman.encode('utf-8')
    print(ds)

    snowman.encode('ascii', 'ignore')
    snowman.encode('ascii', 'replace')
    snowman.encode('ascii', 'backslashreplace')
    snowman.encode('ascii', 'xmlcharrefreplace')

    #caféを表示
    place = 'caf\u00e9'
    print(place)
    type(place)

    #UTF-8形式でエンコードしてplace_bytesという変数に格納する
    place_bytes = place.encode('utf-8')
    print(place_bytes)
    type(place_bytes)
    #バイト列をUnicode形式にデコード
    place2 = place_bytes.decode('utf-8')
    print(place2)
    print('↑これがうまく機能したのはutf-8にエンコードしutf-8からデコードしたから')


    print("7.1.2 書式指定","古いスタイルpython2")
    print('%s' % 42)    #文字列
    print('%d' % 42)    #10進整数
    print('%x' % 42)    #16進整数
    print('%o' % 42)    #8進整数
    print('%f' % 7.03)    #10進float
    print('%e' % 7.03)    #指数形式float
    print('%g' % 7.03)    #10進floatまたは指数形式float
    print('%d%%' % 100)    #リテラルの%

    #文字列と整数の挿入
    actor = 'Richard Gere'
    cat = 'Chester'
    weight = 28

    print("My wife's favorite actor is %s" % actor)
    print("Our cat %s weights %s pounds" % (cat, weight))

    n = 42
    f = 7.03
    s = 'string cheese'
    #python2までのスタイル
    print('%d %f %s' % (n, f, s))

    #python3からのスタイル、
    #順序の指定ができる
    print('{2} {0} {1}'.format(f, s, n))
    # 書式指定を行う
    print('{n} {f} {s}'.format(n=42, f=7.03, s='string cheese'))
    # 使った値を辞書にまとめる
    d = {'n': 42, 'f': 7.03, 's': 'string cheese'}
    # {0}はd,{1}は'other'を表す
    print('{0[n]} {0[f]} {0[s]} {1}'.format(d, 'other'))

    print('7.1.3 \nmatch()による正確なマッチ')
    import re
    source = 'Young Frankenstein'
    m = re.match('You', source)  # matchはsourceの先頭がパターンに一致するかどうかを見る
    if m:  # matchはオブジェクトを返す。マッチした部分を確かめる
        print(m.group())
        print('含まれている')

    m = re.match('^You', source)  # パターンの先頭に^をつけても同じ意味になる
    if m:
        print(m.group())
        print('含まれている')

    print('search()のよる最初のマッチ')
    m = re.search('Frank', source)
    if m:  # searchはオブジェクトを返す
        print('search()結果')
        print(m.group())

    print('findall()のよる最初のマッチ')
    m = re.findall('n', source)
    if m:  # findallはリストを返す
        print('findall()結果')
        print(m)
        print(len(m))

    print('7.2.1  バイトとバイト列')
    blist = [1, 2, 3, 255]
    the_bytes = bytes(blist)
    print(the_bytes)
    the_byte_array = bytearray(blist)
    print(the_byte_array)

    print('\nthe_byte_arrayを書き換える')
    the_byte_array[1] = 127
    print(the_byte_array)

    #オライリーのメガネザル
    import struct
    valid_png_header = b'\x89PNG\r\n\x1a\n'
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + \
        b'\x00\x00\x00\x9a\x00\x00\x00\x8d\x08\x02\x00\x00\x00\xc0'
    if data[:8] ==valid_png_header:
        width,height = struct.unpack('>ll', data[16:24])
        print('valid PNG, width', width, 'height', height)
    else:
        print('Not a valid PNG')

    print('個々の4バイト値は直接検証することができる')
    print(data[16:20])

    #pythonのデータをバイトに変換したい場合にはstructのpack関数を使う
    import struct
    print(struct.pack('>L', 154))
    print(struct.pack('>L', 141))
    #countプレフィックスを使って表す
    print(struct.unpack('>2L',data[16:24]))

    print('ビット演算子')
