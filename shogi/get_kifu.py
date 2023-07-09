#coding: UTF-8
from urllib import request
from bs4 import BeautifulSoup
import json

def scraping():
    #url
    print(get_latest_kifu_url())
    return 
    # url = "https://shogidb2.com/games/bc26fd57bf9ac5f1c48a9e4a99a033f10edffe1a"

    #get html
    html = request.urlopen(url)

    #set BueatifulSoup
    soup = BeautifulSoup(html, "html.parser")

    main_contents = soup.find(class_= "container-fluid")

    # load kifu
    kifu_row_data = main_contents.script.contents[0]
    kifu_row_data = kifu_row_data[kifu_row_data.index("=") + 1: -1]
    json_kifus = json.loads(kifu_row_data)
    json_kifus["moves"] = load_kifu(json_kifus)

    for k, v in json_kifus.items():
        print("{}: {}".format(k, v))

def get_latest_kifu_url():
    url = "https://shogidb2.com/latest"

    #get html
    html = request.urlopen(url)

    #set BueatifulSoup
    soup = BeautifulSoup(html, "html.parser")
    print(soup)

    href_url = soup.find(class_="list-group").find("a").get("href")

    return "https://shogidb2.com/" + href_url

def load_kifu(json_kifus):
    row_moves = [moves_dict["move"] for moves_dict in json_kifus["moves"]]

    moves = []
    for rm in row_moves:
        if rm.find("(") != -1:
            moves.append(rm[:rm.index("(")])
        else:
            moves.append(rm)

    return moves



if __name__ == "__main__": scraping()
