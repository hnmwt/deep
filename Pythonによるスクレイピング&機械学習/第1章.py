import urllib.request

#p26
#urlと保存パスを指定
url = "https://uta.pw/shodou/img/28/214.png"
savename = "test.png"

# ダウンロード
"""
urllib.request.urlretrieve(url, savename)
print("保存しました")
"""

# pythonのメモリに一時保存してからダウンロード
mem = urllib.request.urlopen(url).read()
# 保存
with open(savename, mode= "wb") as f:
    f.write(mem)
    print('保存しました')


#p27
#IP確認APIへアクセスして結果を表示する
import urllib.request
#データを取得する
url = "https://api.aoikujira.com/ip/ini"
res = urllib.request.urlopen(url)
data = res.read()
#バイナリを文字列に変換
text = data.decode("utf-8")
print(text)


#p29
import urllib.request
import urllib.parse

API = "https://api.aoikujira.com/zip/xml/get.php"
#パラメーターをURLエンコードする
values = {
    'fmt': 'xml',
    'zn': '1500042'
}
params = urllib.parse.urlencode(values)
#リクエスト用のURLを生成
url = API + "?" + params
#ダウンロード
data = urllib.request.urlopen(url).read()
text = data.decode("utf-8")
print(text)

"""
#P30,31
import sys
import urllib.request as req
import urllib.parse as parse
#コマンドライン引数を得る
if len(sys.argv) <= 1:
    print("USAGE: 第一章.py (keyword)")
    sys.exit()
keyword = sys.argv[1]   #コマンドライン引数,p32
#パラメーターをURLエンコードする
API = "https://api.aoikujira.com/hyakunin/get.php"
query = {
    "fmt": "ini",
    "key": keyword
}
params = parse.urlencode(query)
url = API + "?" +params
print("url=", url)
#ダウンロード
with req.urlopen(url) as r:
    b = r.read()
    data = b.decode('utf-8')
    print(data)
"""


#p34
from bs4 import BeautifulSoup
#解析したいHTML
html = """
<html><body>
<h1>スクレイピングとは</h1>
<p>webページを解析すること</p>
<p>任意の箇所を抽出すること</p>
</body></html>
"""
#HTMLを解析する
soup = BeautifulSoup(html, 'html.parser')
#任意の部分を抽出する
h1 = soup.html.body.h1
p1 = soup.html.body.p
p2 = p1.next_sibling.next_sibling
#要素のテキストを表示する
print("h1 = " + h1.string)
print("p = " + p1.string)
print("p = " + p2.string)


#p35
from bs4 import BeautifulSoup
html = """
<html><body>
    <h1 id="title">スクレイピングとは</h1>
    <p id="body">Webページから任意のデータを抽出すること</p>
</body></html>
"""
#HTMLを解析する
soup = BeautifulSoup(html, 'html.parser')
#find()メソッドで取り出す
title = soup.find(id="title")
body = soup.find(id="body")
#テキスト部分を抽出
print("#title=" + title.string)
print("#body=" + body.string)


#p36
from bs4 import BeautifulSoup
html = """
<html><body>
    <ul>
        <li><a href="http://uta.pw">uta</a></li>
        <li><a href="http://oto.chu.jp">oto</a></li>
    </ul>
</body></html>
"""
#HTMLを解析する
soup = BeautifulSoup(html, 'html.parser')
#find_all()メソッドで取り出す
links = soup.find_all("a")
#リンク一覧を表示
for a in links:
    href = a.attrs['href']
    text = a.string
    print(text, ">", href)
print(links)


#p37 対話実行環境
from bs4 import BeautifulSoup
soup = BeautifulSoup(
    "<p><a href='a.html'>test</a></p>",
    "html.parser")
#解析が正しくできているか確認
soup.prettify()
#<a>タグを変数aに代入
a = soup.p.a
#attrsプロパティの型を確認
type(a.attrs)
#href属性があるか確認
'href' in a.attrs
#href属性の値を確認
a['href']

print('aの値',a) #※


#p38
from bs4 import BeautifulSoup
import urllib.request as req

url = "https://api.aoikujira.com/zip/xml/1500042"
#urlopen()でデータを取得
res = req.urlopen(url)
#BeautifulSoupで解析
soup = BeautifulSoup(res, 'html.parser')
#任意のデータを抽出
ken = soup.find("ken").string
shi = soup.find("shi").string
cho = soup.find("cho").string
print(ken, shi, cho)


#p39
from bs4 import BeautifulSoup
#解析対象となるHTML
html = """
<html><body>
<div id="meigen">
    <h1>トルストイの名言</h1>
    <ul class="items">
        <li>汝の心に教えよ、心に学ぶな。</li>
        <li>謙虚な人は誰からも好かれる。</li>
        <li>強い人々は、いつも気取らない。</li>
    </ul>
</div>
</body></html>
"""
#HTMLを解析する
soup = BeautifulSoup(html, 'html.parser')
#必要な部分をCSSクエリで取り出す
#タイトル部分を取得
h1 = soup.select_one("div#meigen > h1").string
print("h1 =", h1)
#リスト部分を取得
li_list = soup.select("div#meigen > ul.items > li")
print(li_list)  #※
for li in li_list:
    print("li =", li.string)


#p40 yahooファイナンスの為替情報を取得
from bs4 import BeautifulSoup
import urllib.request as req

url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
#urlopen()でデータを取得
res = req.urlopen(url)
#BeautifulSoupで解析
soup = BeautifulSoup(res, 'html.parser')
#任意のデータを抽出
price = soup.select_one(".stoksPrice").string
print("usd/jpy=", price)


#p46
from bs4 import BeautifulSoup
import urllib.request as req
url = "https://www.aozora.gr.jp/index_pages/person148.html#sakuhin_list_1"
res = req.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')

li_list = soup.select("ol>li")
print(li_list)
for li in li_list:
    a = li.a
    if a != None:
        name = a.string
        href = a.attrs["href"]
        print(name, ">", href)


#p49
from bs4 import BeautifulSoup
fp = open("books.html",encoding="utf-8")
soup = BeautifulSoup(fp, "html.parser")
#cssセレクターで検索する方法
sel = lambda q : print(soup.select_one(q).string)
sel("#nu")
sel("li#nu")
sel("ul > li#nu")
sel("#bible #nu")
sel("#bible > #nu")
sel("ul#bible > li#nu")
sel("li[id='nu']")
sel("li:nth-of-type(4)")
#その他の方法
print(soup.select("li")[3].string)
print(soup.find_all("li")[3].string)


#p50
from bs4 import BeautifulSoup
fp = open()






