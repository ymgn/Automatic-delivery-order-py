# -*- coding: utf-8 -*-

import json

# ここからseleniumでブラウザ操作必要分
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys # 文字を入力する時に使う

#ここからflaskの必要分
import os
from flask import Flask

#ここからflaskでcorsの設定 ajaxを使う時のクロスドメイン制約用
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

driver = webdriver.PhantomJS()

# driver = webdriver.PhantomJS() # PhantomJSを使う 
driver.set_window_size(1124, 850) # PhantomJSのサイズを指定する
driver.implicitly_wait(20) # 指定した要素などがなかった場合出てくるまでdriverが最大20秒まで自動待機してくれる
URL = "https://www.ginsara.jp/menu/"
driver.get(URL) # slideshareのURLにアクセスする

FILENAME1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen1.png") # スクショ用ファイルの場所と名前を定義
FILENAME2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen2.png")
FILENAME3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen3.png")
@app.route('/')
def index():
    return "使い方 : /注文するsushi.jsonの添字番号"

@app.route('/sushi/<int:sushi_num>') # 検索ワード/ページ数をパスから変数に受け取る
def sushi(sushi_num):
    f1 = open('setting.json','r') # settingファイルを読み込み
    setting_data = json.load(f1)
    f2 = open('sushi.json','r') # settingファイルを読み込み
    sushi_data = json.load(f2)
    count = 0
    # ここからアカウントにログイン--------------- 
    login_button = driver.find_element_by_class_name("header_nav-login") # ログインボタンを取得
    login_button.find_element_by_tag_name("a").click() # ログインボタンをクリック
    login_form = driver.find_element_by_id("mail") # mail要素を取得
    login_form.send_keys(setting_data[0]["mail"]) # mailを入力
    login_form = driver.find_element_by_id("password") # mail要素を取得
    login_form.send_keys(setting_data[0]["password"]) # mailを入力
    login_form.submit() # ログインをsubmitする
    print(u"ログイン完了")
    # ログイン処理終了----------------
    # ここからメニューまで移動---------
    menu = driver.find_element_by_class_name("header_utility-menu") # ヘッダーのメニューボタンをクリック
    menu.find_element_by_tag_name("a").click()
    
    # 注文予定の寿司のID分回す
    for data_id in sushi_data[sushi_num]["sushi"]:
        # 一つ一つの寿司を確認していく
        flag = 0    # 目当ての寿司発見フラグを初期化

        # 注文予定の寿司が全て注文できたかどうか
        if len(sushi_data[sushi_num]["sushi"]) > count:
            print(u"メニューだよ")
            print(str(len(sushi_data[sushi_num]["sushi"]))+":len  "+str(count)+":count")
 
            # 上のメニューの桶ボタンをクリックする
            oke_menu = driver.find_element_by_xpath("//div[@class='menu_nav-btn']/a[@href='/menu/category_CO000/']") # 桶ボタンをクリック
            oke_menu.click()
            sushi_list = driver.find_element_by_class_name("menulist") # 寿司のデータが有るリストの親要素を入手
            sushis = sushi_list.find_elements_by_tag_name("li") # 親要素内の寿司のデータをリストで入手
            
            # ここから桶メニューの1商品ずつループ
            for sushi in sushis:
                # 注文する寿司を注文し終わったかどうか判定
                if 0 == flag:
                    # 寿司のタイトルからIDを抽出
                    name = sushi.find_element_by_class_name("menulist_pdct").text
                    if "★" in name :
                        sushi_id = name[0:name.find("★")]
                    else :
                        sushi_id = name[0:name.find("　")]
                    
                    # お目当ての寿司かどうか判定
                    if sushi_id == data_id["id"]:
                        driver.save_screenshot(FILENAME2) # FILENAME 222 にスクショを上書き 
                        print(sushi_id + u"望みの寿司です")
                        print(sushi.text)
                        detail_btn = sushi.find_element_by_class_name("btn-m") # 詳細ボタン
                        detail_btn = detail_btn.find_element_by_tag_name("a") # 詳細ボタンのaタグ
                        detail_btn.click()  # 商品詳細を見るボタンをクリック

                        # ここで注文予定の寿司の詳細に移動============================
                        cart_btn = driver.find_element_by_class_name("js-fadein-button")
                        cart_btn.click()
                        # close_btn = driver.find_element_by_class_name("lv_back")
                        # close_btn = close_btn.find_element_by_tag_name("a")
                        # close_btn.click()
                        flag = 1
                        count += 1
                    else:
                        print(u"違う寿司です")
                else:
                    driver.save_screenshot(FILENAME1) # FILENAMEにスクショを上書き
                    print(u"カートに入れました")
                    break
            else:
                # 商品一覧の中に注文予定の寿司IDが存在しなかった場合の処理
                print(u"注文予定の寿司ID"+data_id["id"]+"が見つからなかったためパスします。")

    # driver.close() # ブラウザ操作を終わらせる
    return u"注文したよ！"
 
 
# bashで叩いたかimportで入れたかを判定する
if __name__ == '__main__':
    app.run()