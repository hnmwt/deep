from 競馬 import A01準備

import requests
import os
import time
import csv
from bs4 import BeautifulSoup



#-----------------------------設定する変数---------------------------------------------------
#出馬情報リンクを代入
race_url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=202030110310&rf=race_list'

#出馬頭数を代入
tousu = 12

#-----------------------------設定する変数---------------------------------------------------

A01準備.Zizensakujo()              #前回の残りファイルを削除
A01準備.Zentai_Syutoku(race_url, tousu)  #デファインparser_syutokuを実行
A01準備.Yomikomi()                      #デファインYomikomiを実行

print("データを作成しました")

