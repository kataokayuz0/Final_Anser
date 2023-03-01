# モジュールのインポート
import pandas as pd
import re
import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import ssl
import socket
from urllib.parse import urlparse


options = Options()
options.add_argument('--headless')
driver_path = ChromeDriverManager().install()
browser = webdriver.Chrome(executable_path=driver_path, options=options)

# 大阪府の居酒屋を対象に調査
# HTMLデータの取得(1ページ目)
time.sleep(3)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
browser.get('https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B')

# 全ての<a>要素を取得し、href属性の値を取得する
linkslist = []
links = browser.find_elements(By.CSS_SELECTOR, "a.style_titleLink__oiHVJ")
for link in links:
    href = link.get_attribute('href')
    if (href and href not in linkslist):
        linkslist.append(href)

# HTMLデータの取得(2ページ目)
time.sleep(3)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
browser.get('https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=2')

# 全ての<a>要素を取得し、href属性の値を取得する
links = browser.find_elements(By.CSS_SELECTOR, "a.style_titleLink__oiHVJ")
for link in links:
    href = link.get_attribute('href')
    if (href and href not in linkslist):
        linkslist.append(href)

# HTMLデータの取得(3ページ目)
time.sleep(3)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
browser.get('https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=3')

# 全ての<a>要素を取得し、href属性の値を取得する
links = browser.find_elements(By.CSS_SELECTOR, "a.style_titleLink__oiHVJ")
for link in links:
    href = link.get_attribute('href')
# 50店舗で停止
    if (len(linkslist) == 50):
        break
    if (href and href not in linkslist):
        linkslist.append(href)


# HTMLデータの取得(4ページ目)
time.sleep(3)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
browser.get('https://r.gnavi.co.jp/area/aream3102/rs/?date=20230307&time=1900&people=2&fw=%E5%B1%85%E9%85%92%E5%B1%8B&p=4')

# 全ての<a>要素を取得し、href属性の値を取得する
links = browser.find_elements(By.CSS_SELECTOR, "a.style_titleLink__oiHVJ")
for link in links:
    href = link.get_attribute('href')
    # 50店舗で停止
    if (len(linkslist) == 50):
        break
    if (href and href not in linkslist):
        linkslist.append(href)

print(linkslist)
lists = [[] for _ in range(50)]

# リストのurlから情報を取得
# Chrome WebDriverを初期化
options = Options()
options.add_argument('--headless')  # ヘッドレスモードで実行する
browser = webdriver.Chrome(options=options)
for i in range(0, 50):
    browser.get(linkslist[i])

    # 店名を表示
    names = browser.find_elements(By.CLASS_NAME, "fn")
    name = [element.text for element in names]
    name = ', '.join(name)
    if name:
        print(name)
    else:
        print("")

    # 電話番号を表示
    phone_numbers = browser.find_elements(By.CLASS_NAME, "number")
    phone_number = [element.text for element in phone_numbers]
    phone_number = ', '.join(phone_number)
    if phone_number:
        print(phone_number)
    else:
        print("")

    # メールアドレスを表示
    try:
        email = browser.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]').get_attribute('href').replace('mailto:', '') 
        print(email)
    except:    
        email = ""
        print(email)

    # 都道府県を表示
    kens = browser.find_elements(By.CLASS_NAME, "region")
    kens = [element.text for element in kens]
    if kens:
        ken = kens[0][:3]
        print(ken)
    else:
        print("")

    # 市区町村を表示
    if kens:
        kens_str = kens[0]
        city = kens_str[3:]
        city = re.sub(r'\d|-', '', city)
        print(city)
    else:
        print("")

    # 番地を表示
    if kens:
        kens_str = ''.join(kens)
        city_str = ''.join(city)
        address = kens_str.replace(ken, '').replace(city_str, '')
        print(address)
    else:
        print("")

    # 建物名を表示
    buildings = browser.find_elements(By.CLASS_NAME, "locality")
    building = [element.text for element in buildings]
    building = ', '.join(building)
    if building:
        print(building)
    else:
        print("")

    # ページのURLを取得
    try:
        element = browser.find_element(By.CLASS_NAME, 'url')
        page_url = element.get_attribute('href')
        print(page_url)
        browser.get(page_url)
        parsed_url = urlparse(page_url)
        addrinfo = socket.getaddrinfo(
            parsed_url.netloc, 443, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)[0]
        ip_address = addrinfo[4][0]
        print("IP Address: ", ip_address)
        context = ssl.create_default_context()
        # ssl証明書の判定
        with socket.create_connection((ip_address, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=parsed_url.netloc) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    has_ssl_certificate = "TRUE"
                    print(has_ssl_certificate)
                else:
                    has_ssl_certificate = "FALSE"
                    print(has_ssl_certificate)
    #SSLで保護されていないページ，もしくはhtmlと証明書のIPアドレスが異なる場合には停止                
    except ssl.SSLError:
        has_ssl_certificate = "FALSE"
        print(has_ssl_certificate)
    #何も記載がない場合には空白を出力    
    except NoSuchElementException:
        page_url = ""
        has_ssl_certificate = ""
        print(page_url)
        print(has_ssl_certificate)

        

    lists[i] = [name, phone_number, email, ken, city,
                address, building, page_url, has_ssl_certificate]

# CSVファイルに書き込む
with open('成果物：1-2.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['店舗名', '電話番号', 'メールアドレス', '都道府県',
                    '市区町村', '番地', '建物名', 'URL', 'SSL'])
    for j in range(50):
        writer.writerow(lists[j])

# dataframe形式で表示
df = pd.read_csv('成果物：1-2.csv', index_col=0)

print(df)

