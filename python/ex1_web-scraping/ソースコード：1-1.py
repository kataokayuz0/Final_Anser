# モジュールのインポート
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import unicodedata

# 検索キーワードをユーザから入力する
freeword = input('県名などの検索フリーワードを入力してください：')

# 検索URLのテンプレート
url_template = 'https://r.gnavi.co.jp/area/jp/rs/?fw={}&p={}'

# ページ番号
page = 1

# 店舗のURLを格納するリスト
linkslist = []

#ユーザーエージェントの指定
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'}
# 検索URL
url = url_template.format(freeword, page)
time.sleep(5)
# リクエストを送信
res = requests.get(url)
# レスポンスからHTMLを抽出
soup = BeautifulSoup(res.content, 'html.parser')


while len(linkslist) < 50:
    # 全ての<a>要素を取得し、href属性の値を取得する
    links = soup.find_all('a', class_="style_titleLink__oiHVJ")
    for link in links:
        href = link.get('href')
        if (href and href not in linkslist and len(linkslist) < 50):
            linkslist.append(href)

    page += 1
    # 検索URL
    url = url_template.format(freeword, page)
    time.sleep(5)
    # リクエストを送信
    res = requests.get(url)
    # レスポンスからHTMLを抽出
    soup = BeautifulSoup(res.content, 'html.parser')

lists = [[] for _ in range(len(linkslist))]
#リストのurlから情報を取得
for i in range(0, len(linkslist)):
    res = requests.get(linkslist[i])
    soup = BeautifulSoup(res.content, 'html.parser')

    #店名を表示
    names = soup.find('p', class_='fn org summary')
    if names:
        name = names.text
        print(name)
    else:
        print("")

    #電話番号を表示
    phone_numbers = soup.find('span', class_='number')
    if phone_numbers:
        phone_number = phone_numbers.text
        print(phone_number)
    else:
        print("")

    #メールアドレスを表示
    email=[]
    print(email)

    # 都道府県を表示
    kens = soup.find('span', class_='region')
    if kens:
        address = kens.text
        pattern = r'^.+?[都道府県]'
        match = re.match(pattern, address)
        if match:
            ken = match.group()
        else:
            print("都道府県名が見つかりませんでした。")
        print(ken)
    else:
        print("")

    # 番地を表示
    if kens:
        kens_str = ''.join(kens)
        address2 = kens_str.replace(ken, '')
        pattern = r'[\d－-]+'
        match = re.search(pattern, address2)
        if match:
            address = match.group()
        else:
            print("番地が見つかりませんでした。")
    else:
        print("")

    # 市区町村を表示
    if kens:
        kens_str = ''.join(kens)
        address_str = ''.join(address)
        city = kens_str.replace(ken, '').replace(address, '')
        print(city)
        if address:
            address = '="{0}"'.format(address)
            print(address)
        else:
            address = ""
            print(address)
    else:
        print("")





    #建物名を表示
    buildings = soup.find('span', class_='locality')
    if buildings:
        building = buildings.text
        print(building)
    else:
        building =""
        print(building)

    #URLを表示
    url=[]
    print(url)   

    #SSLの有無を表示
    ssl=[]
    print(ssl)

    lists[i] = [name, phone_number, "", ken, city,
                address, building, "", ""]


# CSVファイルに書き込む
with open('成果物：1-1.csv', mode='w', encoding='cp932', errors='ignore', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['店舗名', '電話番号', 'メールアドレス', '都道府県',
                    '市区町村', '番地', '建物名', 'URL', 'SSL'])

    for j in range(len(linkslist)):
        # CSVファイルに書き込む
        writer.writerow(lists[j])

# dataframe形式で表示
df = pd.read_csv('成果物：1-1.csv', encoding='cp932', index_col=0)

print(df)
