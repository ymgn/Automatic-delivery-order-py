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

# スクショ用のファイル設定
FILENAME1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1_トップページ.png")
FILENAME2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2_ログインページ.png")
FILENAME3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3_ログイン完了後.png")
FILENAME4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "4_商品詳細.png")
FILENAME5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "5_商品カート.png")
FILENAME6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "6_注文確定.png")

@app.route('/')
def index():
    return "使い方 : /注文するsushi.jsonの添字番号"

@app.route('/sushi/<int:sushi_number>') # sushiの設定ファイルの番号をパスから変数に受け取る
def sushi(sushi_number):
    driver = webdriver.PhantomJS() # PhantomJSを使う 
    driver.set_window_size(1124, 850) # PhantomJSのサイズを指定する
    driver.implicitly_wait(10) # 指定した要素などがなかった場合出てくるまでdriverが最大20秒まで自動待機してくれる
    URL = "https://www.ginsara.jp/"
    driver.get(URL) # slideshareのURLにアクセスする
    f1 = open('setting.json','r') # アカウントのsettingファイルを読み込み
    setting_data = json.load(f1)
    f2 = open('sushi.json','r') # 注文リストのsushiファイルを読み込み
    sushi_data = json.load(f2)
    count = 0   # 注文予定の寿司を注文したかどうかのカウント
    driver.save_screenshot(FILENAME1) # 操作前のページをスクリーンショット

    # ここからアカウントにログイン--------------- 
    login_button = driver.find_element_by_class_name("header_nav-login") # ヘッダーのログインボタンを取得
    login_button.find_element_by_tag_name("a").click() # ログインボタンをクリック
 
    # ログインページ====================
    login_form = driver.find_element_by_id("mail") # mail欄要素を取得
    login_form.send_keys(setting_data[0]["mail"]) # mailを入力
    login_form = driver.find_element_by_id("password") # パスワード欄要素を取得
    login_form.send_keys(setting_data[0]["password"]) # パスワードを入力
    driver.save_screenshot(FILENAME2) # ログインページをスクリーンショット
    login_form.submit() # ログインをsubmitする
    print(u"ログインしました")

    # 寿司メニューまで移動
    menu = driver.find_element_by_class_name("header_utility-menu") # ヘッダーのメニューボタン要素を取得
    menu.find_element_by_tag_name("a").click()  # メニューボタンをクリック

    driver.save_screenshot(FILENAME3) # ログイン後商品リストページをスクリーンショット

    # # 注文時間外の場合注文できないので判定できるようにする　まだできていない
    # if driver.find_element_by_class_name("attention_box").is_displayed():
    #     print("errorが表示されています。\n")
    #     error = driver.find_element_by_xpath("//div[@class='attention_box mt10']/p[@class='error']")
    #     print(error.text)
    #     return u"営業時間外のため注文できませんでした。"
    # else:
    #     print("営業時間内です")

    # 注文予定の寿司を一つずつ取り出して回す
    for data_id in sushi_data[sushi_number]["sushi"]:   # 一つ一つの寿司を確認していく
        flag = 0    # 目当ての寿司発見フラグを初期化
        sushi_num = int(data_id["num"]) - 1 # 寿司の注文予定の数
         
        # 寿司の個数が正しい範囲か判定
        if 0>sushi_num or sushi_num > 9:
            print(u" \n 寿司ID:"+ data_id["id"] +" 寿司個数:"+data_id["num"])
            print(u"\n 注文予定の寿司の個数が1以上10以下ではないためをパスします----------------")
            flag = 1
            count += 1 
            
        # 注文予定の寿司が全てカートに入れるまで入る
        if len(sushi_data[sushi_number]["sushi"]) > count:
            
            # 上のメニューの桶ボタンをクリックする
            oke_menu = driver.find_element_by_xpath("//div[@class='menu_nav-btn']/a[@href='/menu/category_CO000/']") # 桶ボタンをクリック
            oke_menu.click()    # 桶メニューを開く
            sushi_list = driver.find_element_by_class_name("menulist") # 寿司のデータが有るリストの親要素を入手
            sushis = sushi_list.find_elements_by_tag_name("li") # 親要素内の寿司のデータをリストで入手
            print(u"\nメニューを見ます")

            # ここから桶メニューの1商品ずつループ
            for sushi in sushis:
                # 注文予定の寿司を注文し終わった場合以降の寿司を検索しないように判定
                if 0 == flag:                    
                    # 寿司のタイトルからIDを抽出
                    name = sushi.find_element_by_class_name("menulist_pdct").text
                    if "★" in name :
                        sushi_id = name[0:name.find("★")]
                    else :
                        sushi_id = name[0:name.find("　")]
                    
                    # お目当ての寿司かどうか判定
                    if sushi_id == data_id["id"]:
                        print(sushi_id + u"　注文予定の寿司を見つけました")
                        # print(sushi.text)
                        detail_btn = sushi.find_element_by_class_name("btn-m") # 詳細ボタンを取得
                        detail_btn = detail_btn.find_element_by_tag_name("a") # 詳細ボタンの中のaタグを抽出
                        detail_btn.click()  # 商品詳細を見るボタンをクリック

                        # ここで注文予定の寿司の詳細に移動============================
                        # 注文予定の数を選択
                        num_btn_list = driver.find_element_by_class_name("form_radio-num")  # 個数ボタンのリストの親要素を取得
                        num_btn = num_btn_list.find_elements_by_class_name("col")   # 個数ボタンをリストで取得
                        num_btn[sushi_num].find_element_by_tag_name("label").click()    # 注文予定数のボタンをクリック
                        cart_in_btn = driver.find_element_by_class_name("js-fadein-button") # カートに入れるボタンの要素を取得
                        cart_in_btn.click() # カートに入れるボタンをクリック
                        flag = 1    # カートに入れたので以降の寿司を検索しないようにフラグを立てる
                        count += 1  # 注文予定の寿司の数をカートにいれたかカウント
                        driver.save_screenshot(FILENAME4) # 商品詳細をスクリーンショット 
                        print(u"寿司をカートに入れました")
                    # else:
                    #     print(u"違う寿司です")    # 違う寿司だった場合
                else:
                    # 注文予定の寿司をカートに入れた場合残りの寿司を検索しない
                    break
            else:
                # 商品一覧の中に注文予定の寿司IDが存在しなかった場合の処理
                print(u"注文予定の寿司ID"+data_id["id"]+"が見つからなかったためパスします。")

            print(str(len(sushi_data[sushi_number]["sushi"]))+"個注文予定  "+str(count)+"個カートに入れました")
    else:
        # 注文予定の寿司を全て商品カートに入れた時
        print(u"\n注文予定の寿司を全て商品カートに入れました")
        cart_btn = driver.find_element_by_class_name("header_nav-cart")
        cart_btn = cart_btn.find_element_by_tag_name("a")
        cart_btn.click()
        
        # カート一覧ページ================
        print(u"カート一覧ページ")
        driver.save_screenshot(FILENAME5) # カート一覧ページをスクリーンショット
        noworder_btn = driver.find_element_by_xpath("//li[@class='col']/label[@onclick='']")    # 今すぐ配達ボタンの要素を取得
        noworder_btn.click()    # 今すぐ配達ボタンをクリック
        gotoorder_btn = driver.find_element_by_id("gotoOrder")  # お支払方法、配達先指定ページへボタン要素を取得
        gotoorder_btn.click()   # お支払方法、配達先指定ページへボタンをクリック
        
        # お支払い方法、配達先指定ページ===============
        print(u"お支払い方法、配達先指定ページ")
        gotostep2_btn = driver.find_element_by_id("gotoStep2")  # ご注文の確認ボタンの要素を取得
        gotostep2_btn.click()   # ご注文の確認ボタンをクリック
        
        # ご注文確認ページ===================
        print(u"ご注文確認ページ")
        driver.save_screenshot(FILENAME6) # 注文確認ページをスクリーンショット
        regist_order = driver.find_element_by_id("regist-order") # 確定ボタンの要素を取得
        ## regist_order.click()  # 配達確定ボタンを押す ======================ここのコメントアウトを外すと確定ボタンを押す===================================== 
        print(u"\n注文を確定しました！")
        
    driver.close() # ブラウザ操作を終わらせる
    return u"注文しました。確認メールが届くのをお待ち下さい\n"
 
 
# bashで叩いたかimportで入れたかを判定する
if __name__ == '__main__':
    app.run()
