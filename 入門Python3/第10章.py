def 第10章():
    print('\n\n第10章')

    # 10章で使うファイルの作成
    fout = open('Oops.txt', 'wt')
    print('Oops, I created a file.', file=fout)
    fout.close()
    print('Oops.txt作成')

    print('exists()によるファイルが存在することのチェック')
    import os
    # trueを返す
    os.path.exists('Oops.txt')
    # trueを返す
    os.path.exists('./Oops.txt')
    # falseを返す
    os.path.exists('waffles')
    # trueを返す
    os.path.exists('..')  # ドット１個はカレントディレクトリを表すため必ずtrueになる
    # trueを返す
    os.path.exists('../..')  # ドット2個は親ディレクトリを表すため必ずtrueになる

    print('ファイルタイプのチェック')
    # ファイルかチェック
    name = 'Oops.txt'
    os.path.isfile(name)  # trueを返す
    # ディレクトリかチェック
    os.path.isdir(name)  # falseを返す

    # isabs()は引数が絶対パスかどうか返してくる。引数は存在するファイルでなくても構わない。
    os.path.isabs(name)  # false
    os.path.isabs('/big/fake/name')  # true
    os.path.isabs('big/fake/name/without/a/leading/slash')  # false

    print('copy()によるコピー')
    import shutil
    shutil.copy('Oops.txt', 'ohno.txt')
    print('Oops.txtをohno.txtにコピーする')

    # 　↓　unixコマンドのためやらない
    """ print('rename()によるファイル名の変更')
    import os
    os.rename('ohno.txt', 'ohwell.txt') #ohno.txtのファイル名をohwell.txtに変更
    """

    """print('ハードリンクの作成')
    os.link('Oops.txt', 'yikes.txt')
    os.path.isfile('yikes.txt')
    """

    """ 
    print('シンボリックリンクの作成')
    os.symlink('Oops.txt', 'yikes.txt')
    os.path.islink('jeeper.txt')
    """
    # 　↑　unixコマンドのためやらない

    # abspath()によるパス名の取得、相対パスを絶対パスにして返す
    print(os.path.abspath('Oops.txt'))

    # remove()によるファイルの削除
    os.remove('Oops.txt')
    print(os.path.exists('Oops.txt'))  # 削除を確認 falseを返す


def 第10章区切り():
    import os
    import shutil

    # 実行するときに前回のフォルダが存在していたらツリーごと消す
    if os.path.exists('../poems'):
        shutil.rmtree('../poems/')

    # mkdirによるディレクトリの作成
    os.mkdir('../poems')
    print(os.path.exists('../poems'))

    # rmdir()によるディレクトリの削除
    os.rmdir('../poems')
    print(os.path.exists('../poems'))

    # listdir()による内容リストの作成
    os.mkdir('../poems')
    os.listdir('../poems')  # ディレクトリに含まれる内容を取得
    os.mkdir('../poems/mcintype')  # サブディレクトリの作成
    os.listdir('../poems')

    fout = open('../poems/mcintype/the_good_man', 'wt')
    fout.write('''Cheerful and happy was his mood,
    He to the poor was kind and good,
    And he oft' times did find them food
    ''')
    fout.close()
    print(os.listdir('../poems/mcintype'))  # printで作ったファイルの確認をする

    # chdir()によるカレントディレクトリの変更
    os.chdir('../poems')
    print(os.listdir('..'))  # printでカレントディレクトリの変更を確認する

    # glob()によるパターンにマッチするファイルのリストの作成
    import glob
    print(glob.glob('m*'))  # print
    print(glob.glob('??'))  # print

    # 10.3 プログラムとプロセス
    import os
    print(os.getpid())  # インタープリタのID
    print(os.getcwd())  # インタープリタのカレントディレクトリ
    # print(os.getuid())#自分のユーザーID
    # print(os.getgid())#自分のグループID

    #unixのため
    '''import subprocess
    ret = subprocess.getoutput('date')#dateプログラムの出力(unix)
    ret'''


    #↓なぜかうまくいかない
    ''' # multiprocessingによるプロセスの作成
    import multiprocessing
    import os

    def do_this(what):
        whoami(what)

    def whoami(what):
        print("Process %s says: %s" % (os.getpid(), what))

    if __name__ == '__main__':
        whoami("I'm the main program")
        for n in range(4):
            p = multiprocessing.Process(target=do_this, args=("I'm function %s" % n,))
            p.start()'''



