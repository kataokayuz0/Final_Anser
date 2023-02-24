# モジュールのインポート
import requests
from bs4 import BeautifulSoup
import re
import csv
import time

#大阪府を対象に調査
# HTMLデータの取得(1ページ目)
time.sleep(3)
res = requests.get(
    'https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B')
soup = BeautifulSoup(res.content, 'html.parser')

# 全ての<a>要素を取得し、href属性の値を取得する
linkslist = []
links = soup.find_all('a', class_="style_titleLink__oiHVJ")
for link in links:
    href = link.get('href')
    if (href and href not in linkslist):
        linkslist.append(href)

# HTMLデータの取得(2ページ目)
time.sleep(3)
res = requests.get(
    'https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=2')
soup = BeautifulSoup(res.content, 'html.parser')

# 全ての<a>要素を取得し、href属性の値を取得する
links = soup.find_all('a', class_="style_titleLink__oiHVJ")
for link in links:
    href = link.get('href')
    if (href and href not in linkslist):
        linkslist.append(href)

# HTMLデータの取得(3ページ目)
time.sleep(3)
res = requests.get(
    'https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=3')
soup = BeautifulSoup(res.content, 'html.parser')

# 全ての<a>要素を取得し、href属性の値を取得する
links = soup.find_all('a', class_="style_titleLink__oiHVJ")
for link in links:
    href = link.get('href')
    if (href and href not in linkslist):
        linkslist.append(href)
#50店舗で停止        
    if(len(linkslist)==50):
        break  

# HTMLデータの取得(4ページ目)
time.sleep(3)
res = requests.get(
    'https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=4')
soup = BeautifulSoup(res.content, 'html.parser')

# 全ての<a>要素を取得し、href属性の値を取得する
links = soup.find_all('a', class_="style_titleLink__oiHVJ")
for link in links:
    href = link.get('href')
    # 50店舗で停止
    if (len(linkslist) == 50):
        break
    if (href and href not in linkslist):
        linkslist.append(href)


lists = [[] for i in range(50)]

#リストのurlから情報を取得
for i in range(0, 50):
    res = requests.get(linkslist[i])
    soup = BeautifulSoup(res.content, 'html.parser')

    #店名を表示
    title = soup.title.text
    tenmei = title.split(' - ')[0]
    print(tenmei)

    #電話番号を表示
    phone_numbers = soup.find_all('span', class_='number')
    if phone_numbers:
        phone_number = phone_numbers[0].text
        print(phone_number)
    else:
        print("")

    #メールアドレスを表示
    email=[]
    print(email)

    #都道府県を表示
    kens = soup.find_all('span', class_='region')
    if kens:
        ken = kens[0].text[:3]
        print(ken)
    else:
        print("")

    # 市区町村を表示
    if kens:
        city = kens[0].text[3:]
        city = re.sub(r'\d|-', '', city)
        print(city)
    else:
        print("")
    
    #番地を表示
    if kens:
        address = kens[0].text.replace(ken, '').replace(city, '')
        print(address)
    else:
        print("")

    #建物名を表示
    buildings = soup.find_all('span', class_='locality')
    if buildings:
        building = buildings[0].text
        print(building)
    else:
        print("")

    #URLを表示
    url=[]
    print(url)   

    #SSLの有無を表示
    ssl=[]
    print(ssl)

    lists[i] = [tenmei, phone_number, email, ken, city, address, building, url, ssl]


#CSVファイルに書き込む
with open('成果物：1-1.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['店舗名', '電話番号', 'メールアドレス', '都道府県', '市区町村', '番地', '建物名', 'URL', 'SSL'])
    for j in range(50):
        writer.writerow(lists[j])  