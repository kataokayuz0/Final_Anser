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
from selenium.webdriver.common.keys import Keys
import ssl
import socket
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')  # ヘッドレスモードで実行する
options.add_argument('--disable-site-isolation-trials')
driver_path = ChromeDriverManager().install()
browser = webdriver.Chrome(executable_path=driver_path, options=options)



time.sleep(3)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
browser.get('https://www.gnavi.co.jp/')

# 検索ボックスを特定し、入力する文字列を指定する
area = input('エリアを入力してください：')
wait = WebDriverWait(browser, 20)
search_box = wait.until(
    EC.presence_of_element_located((By.ID, 'js-suggest-area')))
search_box.send_keys(area)

#検索を実行する
button = WebDriverWait(browser, 5).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "js-search")))
button.click()
current_url = browser.current_url

#店舗のurlを格納するリスト
linkslist = []

# 全ての<a>要素を取得し、href属性の値を取得する
r = 2
while len(linkslist) < 50:
    time.sleep(3)
    links = browser.find_elements(By.CSS_SELECTOR, "a.style_titleLink__oiHVJ")
    for link in links:
        href = link.get_attribute('href')
        if (href and href not in linkslist and len(linkslist) < 50):
            linkslist.append(href)

    # 次のページに移動 
    new_url = "{}&p={}".format(current_url, r)
    r = r + 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    browser.get(new_url)



print(linkslist)
print(len(linkslist))
lists = [[] for _ in range(len(linkslist))]

# リストのurlから情報を取得
# Chrome WebDriverを初期化
options = Options()
options.add_argument('--headless')  # ヘッドレスモードで実行する
options.add_argument('--disable-site-isolation-trials')
browser = webdriver.Chrome(executable_path=driver_path, options=options)
for i in range(0, len(linkslist)):
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
        address = kens[0]
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
        elements = browser.find_elements(
            By.XPATH, '//a[@title="オフィシャルページ"]')[0]
        if elements:
            page_url = elements.get_attribute("href")
            print(page_url)
        else:
            page_url = ""
            has_ssl_certificate = ""
            print(page_url)
            print(has_ssl_certificate)
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
with open('成果物：1-2.csv', mode='w', encoding='cp932', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['店舗名', '電話番号', 'メールアドレス', '都道府県',
                    '市区町村', '番地', '建物名', 'URL', 'SSL'])

    for j in range(len(linkslist)):
        writer.writerow(lists[j])

# dataframe形式で表示
df = pd.read_csv('成果物：1-2.csv', encoding='cp932', index_col=0)

print(df)

