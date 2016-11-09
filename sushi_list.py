# -*- coding: utf-8 -*-
import scrapelib
import json
import datetime

from bs4 import BeautifulSoup

#一分あたり10リクエストまで
s = scrapelib.Scraper(requests_per_minute=10)

url = "https://www.ginsara.jp/menu/category_CO000/"
#キレイに整える
soup = BeautifulSoup(s.get(url).text,"lxml")
data = []
#全てから１件分のまとまりの配列を出す
#find_allは当てはまる全てを配列にして出す findは初めの1件目だけヒットする
sushi_list = soup.find("ul",class_="menulist")

sushis = sushi_list.find_all("li")

#配列から１件分ずつ出す
for sushi in sushis:
    #配列にまとめる用のリスト
    sushi_in = {}
    #１件分の中からタイトルだけを抽出
    name = sushi.find("p",class_="menulist_pdct")
    #タイトルを入れる
    sushi_in["name"] = name.string
    # 商品IDを取得
    if "★" in name.string :
        sushi_in["id"] = name.string[0:name.string.find("★")]
    else :
        sushi_in["id"] = name.string[0:name.string.find("　")]

    # 寿司の値段を取る
    price = sushi.find("span",class_="tax")
    sushi_in["price"] = price.string[1:-1]
    # 寿司の情報を取る
    info = sushi.find("p",class_="menuinfo_price-text")
    sushi_in["info"] = info.string
    # 寿司のURLを取る
    url = sushi.find("div",class_="menulist_pic").find("a").get("href")
    sushi_in["url"] = url

    data.append(sushi_in)
    
# dampsはjson文字列に変更する関数
jsonstring = json.dumps(data,ensure_ascii=False,indent=2)
#print(jsonstring)
d = datetime.datetime.today()

f = open('%s-%s-%s' % (d.year, d.month, d.day) +".json", "w")
json.dump(data, f, ensure_ascii=False,indent=2)
