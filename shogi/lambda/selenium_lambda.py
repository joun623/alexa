# coding: UTF-8
from bs4 import BeautifulSoup
import json

shogidb2_url = "https://shogidb2.com"

def load_kifu_urls():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # ブラウザのオプションを格納する変数をもらってきます。
    options = Options()

    # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
    # options.set_headless(True)
    options.add_argument('--headless')
 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    # ブラウザを起動する
    driver = webdriver.Chrome(options=options)

    # ブラウザでアクセスする
    driver.get(shogidb2_url + "/newrecords")

    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')

    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    # idがheikinの要素を表示
    anchors = soup.find_all("a")

    return [anchor.get("href") for anchor in anchors if anchor.get("href").startswith("/games")]

def load_kifu_data(kifu_url_id):
    import requests

    kifu_url = shogidb2_url + kifu_url_id 
    html = requests.get(kifu_url)
    soup = BeautifulSoup(html.text, "lxml")
    kifu_data = ""
    for script in soup.find_all("script"):
        if script.string is not None and script.string.startswith("var"):
            kifu_data = script.string
   
    return kifu_data

def load_kifu(json_kifus):
    row_moves = [moves_dict["move"] for moves_dict in json_kifus["moves"]]

    moves = []
    for rm in row_moves:
        if rm.find("(") != -1:
            moves.append(rm[:rm.index("(")])
        else:
            moves.append(rm)

    return moves


if __name__ == "__main__":
    new_kifus = load_kifu_urls()
    kifu_row_data = load_kifu_data(new_kifus[0])
    kifu_row_data = kifu_row_data[kifu_row_data.index("=") + 1: -1]
    json_kifus = json.loads(kifu_row_data)
    json_kifus["moves"] = load_kifu(json_kifus)

    print(json_kifus["moves"])
