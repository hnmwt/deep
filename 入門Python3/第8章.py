def 第8章():
    print('\n\n8章　データの行き先\n')

    print('write()によるテキストファイルへの書き込み')

    poem = '''There was a young lady named Bright,
    Whose speed was far faster than light,
    She started one day
    In a relative way,
    And returned on the previous night.'''
    print(len(poem))

    fout = open('relativity', 'wt')
    fout.write(poem)
    #print()でテキストファイルに書き込むこともできる
    print(poem, file=fout)
    fout.close()
    print('書き込み完了\n')

    print('ソース文字列が大きい場合は全部書き込むまでチャンクに分けて書き込んでいくこともできる')
    fout = open('relativity', 'wt')
    size = len(poem)
    offset = 0
    chunk = 100
    while True:             #無限ループ (offset > sizeの時に終了)
        if offset > size:   #offset > sizeの時は書き込みが完了しているためbreakする
            break
        fragment = fout.write(poem[offset:offset+chunk])   #1回目は100文字書き込む、2回目は残りの66文字を書き込む
        print(fragment,'書き込んだ文字')
        offset += chunk                         #offsetを0→100にする
    fout.close()

    print('\nファイル読み出し')
    fin = open('relativity', 'rt')
    poem = fin.read()
    fin.close()
    print(len(poem))

    print('\n字数を制限してファイル読み出し')
    poem = ''
    fin = open('relativity', 'rt')
    chunk = 100
    while True:
        fragment = fin.read(chunk)
        print(fragment,'\n↑読み込んだ文字')
        if not fragment:
            break
        poem += fragment
    fin.close()
    print('\npoemの文字数→',len(poem))

    #readline()を使うことでファイルを一行ずつ読み出すことができる
    poem =''
    fin = open('relativity', 'rt')
    chunk = 100
    while True:
        line = fin.readline()  #1行ずつ読み出し
        if not line:
            break
        poem += line            #poemは読み込んだline数
    fin.close()
    print('\n読込み完了', len(poem))

    #テキストファイルを最も簡単に読み出す方法
    poem = ''
    fin = open('relativity', 'rt')
    for line in fin:
        poem += line
    fin.close()
    print('テキストファイルを最も簡単に読み出す方法',len(poem))

    #readlines()は一度に一行ずつ読みだして1行文字列のリストを返す
    fin = open('relativity', 'rt')
    lines = fin.readlines()
    fin.close()
    print(len(lines), '行読み込んだ')
    for line in lines:
        print(line, end='')

    #writeによるバイナリファイルの書き込み
    bdata = bytes(range(0, 256))
    print('\n\n',len(bdata))

    fout = open('bfile', 'wb')
    fout.write(bdata)
    fout.close()
    print('バイナリ書き込み完了')

    fout = open('bfile', 'wb')
    size=len(bdata)
    offset=0
    chunk=100
    while True:
        if offset >size:
            break
        # bdataの引数をスライスで指定している、一回目は[0:100],2回目[100:200]
        w = fout.write(bdata[offset:offset+chunk])
        print(w,'文字書き込み完了')
        offset+=chunk
    fout.close()

    print('seek()による位置の変更')
    fin = open('bfile', 'rb')
    print(fin.tell())
    fin.seek(255)
    bdata = fin.read()
    len(bdata)
    bdata[0]
    print('255バイト目',bdata)

    #構造化されたテキストファイル
    print('\ncsvの読み書き')

    import csv
    villains = [
        ['Doctor', 'No'],
        ['Rosa', 'Klabb'],
        ['Mister', 'Big'],
        ['Auric', 'Goldfinger'],
        ['Ernst', 'Blofeld'],
        ]
    with open('villains', 'wt', newline='') as fout: #windowsではnewlines=''をつけることでファイルの1行空白を消すことができる
        csvout = csv.writer(fout)
        csvout.writerows(villains)
    print('書き込み完了')

    print('↑で作ったvillainsファイルを読み出して元のデータ構造を作る')
    with open('villains', 'rt') as fin:
        cin = csv.reader(fin)
        villains = [row for row in cin] #リスト内包表記
    print(villains)

    #辞書のリストにすることもできるDictreader,Dictwriter
    print('読込み')
    with open('villains', 'rt', newline='') as fin:
        cin = csv.DictReader(fin, fieldnames=['first', 'last'])
        villains = [row for row in cin]
        columns = villains
    print(villains)

    print('csvファイルを書きなおす.writeheader()も呼び出す')
    villains = [
        {'first': 'Doctor', 'last': 'No'},
        {'first': 'Rosa', 'last': 'Klabb'},
        {'first': 'Mister', 'last': 'Big'},
        {'first': 'Auric', 'last': 'Goldfinger'},
        {'first': 'Ernst', 'last': 'Blofeld'}
       ]
    with open('villains', 'wt', newline='') as fout:
        cout = csv.DictWriter(fout, ['first', 'last'])#辞書のキー(first,last)をヘッダーにしてファイルに書き込み
        cout.writeheader()
        cout.writerows(villains)

    with open('villains', 'rt') as fin:
        cin = csv.DictReader(fin, fieldnames=['first', 'last'])
        villains = [row for row in cin]
    print(villains)


    #8.2.2 XML

    
