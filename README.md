# お寿司を自動で注文してくれるマン(仮)

## 説明
URLに**curl**などでアクセスするだけで、settingファイルに記入しているアカウントにログインし、
sushiファイルに記入しておいた注文予定の寿司を注文してくれるAPIです。

やってることとしては、SeleniumでPhantomJSを動かし、銀のさらのページを自動で操作し、
ログイン、商品をカートに入れる、注文確定　までをおこなってくれるものとなります。

[銀のさら](https://www.ginsara.jp/)のアカウントに登録している住所に配達します。
選択できる商品は銀のさらに登録されている「桶」カテゴリの商品のみです。

関西オープンフォーラム2016のITCreate部ブースにて展示しました。

## 用意するもの
.exampleと付いているファイルは「.example」を外して、仮の内容をお望みのように書き換えてください。

### setting.json
「銀のさら」に登録したメールアドレスとパスワードを用意しておきます。

### sushi.json
**sushi_list.py**を起動することで「銀のさら」の商品のデータのJsonができます。
使用するのに必須ではありませんが、商品名・商品ID・URL・値段・寿司の個数
のデータをまとめて抽出できるため、参考にしてみてください。

その寿司リストや、公式の商品欄を参考にしつつ注文したい寿司のIDを**sushi.json**に登録してください
一度に注文できる個数は銀のさらで注文できる1〜10個となります。

複数の注文セットを登録することができ、URLの sushi/ の後に、
ファイル内の配列の昇順にあたる、上を ０ として順番を指定することができます。

## 使い方
sushi/[注文したいsyshi.jsonの添字]

にアクセスすると自動で注文(の寸前まで)してくれます。

動作は起動している際にprintされる結果と、スクリーンショットで確認できます。
ソースコードの下の方にある確定ボタンをクリックするコードのコメントアウトを外すと実際に注文できるようになります。

※銀のさらの都合上、営業時間外に動かしてもカートに商品が入らないため、正常に動きません。