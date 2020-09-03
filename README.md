
# AmatsukazeNotifier

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/01.jpg)

Amatsukaze から LINE や Twitter（ツイート・DM）に通知を送れるツールです。

## About・Feature

[Amatsukaze](https://github.com/nekopanda/Amatsukaze) のバッチファイル実行機能を使い、


- LINE (LINE Notify)
- Twitter (ツイート)
- Twitter (ダイレクトメッセージ)

に Amatsukaze の各通知を送信できる Python 製ツールです。
tsukumijima氏の[EDCBNotifier](https://github.com/tsukumijima/EDCBNotifier)を元に制作しました。

Amatsukaze のバッチファイル実行機能を利用しているため、変換処理の実行前後に通知を送る事が可能です。

たとえば、Amatsukaze でエンコードが開始された旨を通知したり、実行結果の一部の情報を送信するといった事が可能です。

LINE への通知は LINE Notify を使って送信します。  
LINE Notify はアプリケーションからの通知を指定したユーザーやグループで受信することができるサービスです。  
通知メッセージは LINE Notify の公式アカウントから受信できます（一度使ってみたほうが早いかも）。

Twitter への通知はツイートでの通知に加え、ダイレクトメッセージでの送信も可能です。  
ダイレクトメッセージは自分宛てに送ることも、DM を送信できる他のアカウントに送ることもできます。  
たとえば、録画通知用の Twitter アカウントを作ってメインアカウントと相互フォローになり、録画通知用のアカウントからメインアカウント宛てに通知を送ることもできます。

通知できるイベントは、

- 変換を開始したとき (実行前_AmatsukazeNotifier.bat が実行されたとき)
- 変換が成功したとき (処理完了状態で実行後_AmatsukazeNotifier.bat が実行されたとき)
- 変換が失敗したとき (処理失敗状態で実行後_AmatsukazeNotifier.bat が実行されたとき)

の 3つです。

それぞれのイベントは、個別に通知するかどうかを設定できます。  
EDCBNotifierを導入している場合は、録画終了の通知後ほぼノータイムで変換開始の通知が送信されることになるので、頻繁に送られて煩いという場合には変換開始のイベントだけ通知しないようにすることも可能です。

通知するメッセージは 3 つのイベントごとに自由に変更できます。  
設定ファイルは Python スクリプトなので、Python の知識があればメッセージをより高度にカスタマイズすることもできそうです。  


基本的にEDCBで録画を行なった場合を想定しているので、その他のソフトを使用して録画したファイルでは正しく動作しない場合があります。
また、AmatsukazeServerとAmatsukazeClientをそれぞれ別のマシンで動作させている場合は正しく動作しない可能性があります。

## Setup

### 1. ダウンロード・配置

<img src="https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/02.png" width="400px">

 \[Code] メニュー内の \[Download Zip] をクリックし、AmatsukazeNotifier をダウンロードします。  
または、[こちら](https://github.com/nukemiri/AmatsukazeNotifier/archive/master.zip) のリンクからでもダウンロードできます。

ダウンロードできたら解凍し、

- AmatsukazeNotifier フォルダ
- bat

を Amatsukaze 本体 (Amatsukaze.vbs) があるフォルダに配置します。  
また、requirements.txt は今後の作業で利用するので、取っておいてください。

### 2. Python のインストール

AmatsukazeNotifier の実行には Python (Python3) が必要です 。動作確認は Python 3.7 系と Python 3.8 系で行っています。

すでに Python3 がインストールされている場合はスキップしても構いませんが、**すでに Python2 がインストールされている場合は別途 Python3 をインストールしてください。**  
（Python2 と Python3 は半分別物で、このうち Python2 は 2020 年 1 月でサポートが終了しています）

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/03.png)

[非公式 Python ダウンロードリンク](https://pythonlinks.python.jp/ja/index.html) から、Python3 のインストーラーをダウンロードします。  
とくにこだわりがないのであれば、**一番上にある Windows (64bit) 用 Python 3.8 の最新版 ( 2020 年 7 月現在の最新は 3.8.5 ) をダウンロードしてください。**  

[Python 公式サイト](https://www.python.org/downloads/windows/) からもダウンロードできますが、わかりにくいので前述のサイトからダウンロードすることをおすすめします。  
Python 公式サイトにも大きいダウンロードボタンがありますが、これは罠です…（OS のビットに関わらず 32bit の インストーラーがダウンロードされる）  

もし OS が 32bit の方は Windows (32bit) 用をダウンロードしてください（ほとんどいないと思うけど…）。  
**Windows10 では Microsoft Store からもインストールすることができますが、安定していない上にストアアプリの制限の影響で正常に動かないことがあるため、非推奨です。**

<img src="https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/04.png" width="600px">

ダウンロードが終わったらインストーラーを実行します。
 \[Install Now] と \[Custom Install] がありますが、 \[Custom Install] の方をクリックしてください。  
このとき、**必ず \[Add Python 3.8 to PATH] にチェックを入れてから進んでください。**

 \[Option Features] は特にこだわりがなければそのまま進みます。  

<img src="https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/05.png" width="600px">

 \[Advanced Options] は ** \[Install for all users] にチェックを入れます**（これで AppData 以下に配置されなくなる）。  
デフォルトでは AppData 以下にユーザーインストールする設定になっていますが、他のユーザーから見れないほかパスが長くなっていろいろ面倒だと思うので、私はおすすめしません。  

 \[Install for all users] にチェックを入れると \[Customize install location] が C:\Program Files\Python38 になりますが、**これも C:\Program Files 以外に変更します。**  
これは C:\Program Files 以下にインストールしてしまうと pip でのライブラリのインストールに毎回管理者権限を求められてしまい面倒なためです。  
私は C:\Applications\Python\Python3.8 にインストールしていますが、とりあえず C:\Program Files 以下と C:\Users 以下でなければよいでしょう（別バージョンを入れることも考え Python\Python3.8 のような階層にしておくのがおすすめ）。

 \[Install] をクリックするとインストールが開始されます。  
 \[Setup was successful] という画面が表示されればインストール完了です。  
試しにコマンドプロンプトや PowerShell から `python -V` と実行してみましょう。

### 3. 依存ライブラリのインストール

AmatsukazeNotifier が必要とする colorama・jaconv・requests・twitter の各ライブラリを pip でインストールします。  

**コマンドプロンプトや PowerShell を開き、`pip install -r (ダウンロードした AmatsukazeNotifier\requirements.txt)` と実行します。**  
または単に `pip install -r colorama jaconv requests twitter` としても構いません。

エラーなくインストールできれば OK です。

### 4. 設定ファイルの作成

Amatsukaze 内に配置した AmatsukazeNotifier フォルダ内の config.default.py は、設定ファイルのひな形になるファイルです。  
config.default.py を config.py にコピーしてください（コピーしておかないと設定が読み込めず動きません）。

リネームでもかまいませんが、設定をミスったときのために config.default.py は取っておくことを推奨します。

### 5. Amatsukaze でバッチを登録

<img src="https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/06.png" width="600px">

Amatsukaze/bat/ に追加した .bat ファイルはAmatsukazeに自動で認識され、頭に "実行前_"と付くものは実行前バッチとして、"実行後_"と付くものは実行後バッチとして登録が可能になります。
プロファイルタブから使用するプロファイルを選んで実行前バッチと実行後バッチの項目に 実行前_AmatsukazeNotifier.bat と 実行後_AmatsukazeNotifier.bat を登録して適用してください。


これでインストールは完了です。

## Usage

AmatsukazeNotifier の設定は AmatsukazeNotifier フォルダ内の config.py にて行います。  
LINE Notify へ通知する場合は LINE Notify のアクセストークンが、Twitter へ通知する場合は Twitter API アプリが必須になります。  
LINE Notify のアクセストークンの作成には LINE へのログインが、Twitter API アプリの作成には Twitter の開発者アカウントがそれぞれ必要です。 

### 1. 設定

config.py を<u>文字コード UTF-8 (BOM 無し)・改行コード LF で編集・保存できるエディタで</u>編集します。  
メモ帳は Windows10 1903 以前のものでは UTF-8 (BOM 無し)・LF で保存できなかったり、またシンタックスハイライトもないため避けてください。  
できれば VSCode などのシンタックスハイライトや lint のあるエディタでの編集を推奨します。

**通知タイプ** (NOTIFY_TYPE) では、LINE (LINE Notify)・Tweet (ツイート)・DirectMessage (ダイレクトメッセージ) から通知するものを選択します。  
デフォルト … 全てに通知する (`['LINE', 'Tweet', 'DirectMessage']`)

**通知を行うイベント** (NOTIFY_EVENT) では、通知するイベントのオン・オフを設定できます。  
ここで設定したイベントだけが通知されます。たとえば頻度の多い PostNotify だけ通知しない設定も可能です。  
デフォルト … 全てオン (`['PostEncStart', 'PostEncSuccess', 'PostEncFailed']`)

**通知時に同時に送信する画像** (NOTIFY_IMAGE) では、通知時に同時に送信する画像を指定できます。   
None に設定した場合は画像を送信しません。画像サイズが大きすぎると送れない場合があるので注意してください（使う機会がない気も…）  
デフォルト … 画像を送信しない (`None`)

**ダイレクトメッセージの宛先** (NOTIFY_DIRECTMESSAGE_TO) では、ダイレクトメッセージで通知する場合に通知を送るアカウントをスクリーンネーム (ID) で指定します。  
@ はつけないでください。予め宛先のアカウントと DM が送信できる状態になっていないと送れません。None に設定した場合は自分宛てに送信します。  
デフォルト … 自分宛てに送信する (`None`)

**ログをファイルに保存するか** (NOTIFY_LOG) では、ログをファイルに保存（出力）するかどうかを設定します。  
True に設定した場合は、ログを config.py と同じフォルダの AmatsukazeNotifier.log に保存します。前回のログは上書きされます。また、コンソールへログを出力しなくなります。  
False に設定した場合は、ログを保存しません。通常通りコンソールにログを出力します。  
デフォルト … ログをファイルに保存しない (`False`)

このほか、config.py 内のコメントも参考にしてください。   
保存する際は 文字コード UTF-8 (BOM 無し)・改行コード LF で保存します（ CR+LF になったり BOM 付きにならないように注意）。

### 2. 通知するメッセージを編集する

通知イベントごとにメッセージを編集できます。  
通知するメッセージの設定は config.py の \[メッセージ] セクションにあります。

EDCBNotifier で使えても AmatsukazeNotifierでは使えないマクロもあるので注意。
独自のマクロも多くあります。
Amatsukaze の[バッチファイル実行機能](https://github.com/nekopanda/Amatsukaze/wiki/%E3%83%90%E3%83%83%E3%83%81%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%AE%9F%E8%A1%8C%E6%A9%9F%E8%83%BD)に環境変数として記載されているものは前後に\$をつければ基本的にそのまま使えます。
実行後バッチでしか利用できないものもあるので注意してください。


使用可能マクロ一覧

#### 実行前、実行後共通
Amatsukaze の環境変数と同じマクロ
- \$ITEM_ID\$ … アイテムに一意に振られるID。追加時、実行前、実行後で同じアイテムを追跡できる。Amatsukazeを再起動するとIDが変わるので注意。
- \$IN_PATH\$ … 入力ファイルパス
- \$OUT_PATH\$ … 出力ファイルパス（拡張子を含まない）
- \$SERVICE_ID\$ … サービスID（チャンネルID）
- \$SERVICE_NAME\$ … サービス名（チャンネル名）
- \$TS_TIME\$ … TSファイルの時刻
- \$ITEM_MODE\$ … モード。Batch…通常 AutoBatch…自動追加 Test…テスト DrcsCheck…DRCSチェック CMCheck…CMチェック
- \$ITEM_PRIORITY\$ … アイテム優先度(1-5)
- \$ITEM_GENRE\$ … 番組ジャンル （[ジャンル] - [詳細ジャンル] の形式 例: アニメ／特撮 - 国内アニメ）
- \$IMAGE_WIDTH\$ … 映像幅
- \$IMAGE_HEIGHT\$ … 映像高さ
- \$EVENT_NAME\$ … 番組名
- \$TAG\$ … Amatsukaze で設定したタグ
- \$PROFILE_NAME\$ … プロファイル名

EDCB 準拠マクロ
- \$Title\$ … 番組名 \$EVENT_NAME\$と同じ
- \$Title2\$ … 番組名（[]の括弧でくくられている部分を削除したもの）
- \$SubTitle\$ … サブタイトル
- \$SID10\$ … ServiceID 10進数 \$SERVICE_ID\$と同じ
- \$SID16\$ … ServiceID 16進数
- \$ServiceName\$ … サービス名(チャンネル名) \$SERVICE_NAME\$と同じ
- \$Genre\$ … 番組のジャンル
- \$SDYYYY\$ … 番組開始日の年4桁
- \$SDYY\$ … 番組開始日の年2桁
- \$SDMM\$ … 番組開始日の月2桁固定
- \$SDM\$ … 番組開始日の月
- \$SDDD\$ … 番組開始日の日2桁固定
- \$SDD\$ … 番組開始日の日
- \$SDW\$ … 番組開始日の曜日
- \$STHH\$ … 番組開始時刻の時2桁固定
- \$STH\$ … 番組開始時刻の時
- \$STMM\$ … 番組開始時刻の分2桁固定
- \$STM\$ … 番組開始時刻の分
- \$STSS\$ … 番組開始時刻の秒2桁固定
- \$STS\$… 番組開始時刻の秒
- \$EDYYYY\$ … 番組終了日の年4桁
- \$EDYY\$ … 番組終了日の年2桁
- \$EDMM\$ … 番組終了日の月2桁固定
- \$EDM\$ … 番組終了日の月
- \$EDDD\$ … 番組終了日の日2桁固定
- \$EDD\$ … 番組終了日の日
- \$EDW\$ … 番組終了日の曜日
- \$ETHH\$ … 番組終了時刻の時2桁固定
- \$ETH\$ … 番組終了時刻の時
- \$ETMM\$ … 番組終了時刻の分2桁固定
- \$ETM\$ … 番組終了時刻の分
- \$ETSS\$ … 番組終了時刻の秒2桁固定
- \$ETS\$ … 番組終了時刻の秒

EDCBNotifier 準拠マクロ
- \$HashTag\$ … 放送局名から取得したハッシュタグ (ハッシュタグは utils.py の get_hashtag() メソッドで定義) 
- \$ServiceNameHankaku\$ … サービス名（チャンネル名） 英数半角
- \$EventNameHankaku\$ … 番組名 英数半角
- \$TitleHankaku\$ … $Title$（番組タイトル）の英数字を半角に変換したもの
- \$Title2Hankaku\$ … $Title2$（番組タイトル・[]で囲まれている部分を削除したもの）の英数字を半角に変換したもの
- \$TimeYYYY\$ … 実行時刻の上2桁付き西暦年 (ex: 2020 (年)) $TimeYY$ … 実行時刻の上2桁なし西暦年 (ex: 20 (年))
- \$TimeMM\$ … 実行時刻の2桁固定の月 (ex: 07 (月)) $TimeM$ … 実行時刻の月 (ex: 7 (月))
- \$TimeDD\$ … 実行時刻の2桁固定の日 (ex: 09 (日)) $TimeD$ … 実行時刻の日 (ex: 9 (日))
- \$TimeW\$ … 実行時刻の曜日 (ex: 火 (曜日))
- \$TimeHH\$ … 実行時刻の2桁固定の時 (24時間) (ex: 06 (時)) $TimeH$ … 実行時刻の日 (ex: 6 (時))
- \$TimeII\$ … 実行時刻の2桁固定の分 (ex: 08 (分)) $TimeI$ … 実行時刻の分 (ex: 8 (分))
- \$TimeSS\$ … 実行時刻の2桁固定の秒 (ex: 02 (秒)) $TimeS$ … 実行時刻の分 (ex: 2 (秒))

AmatsukazeNotifier 独自マクロ
- \$InFolderPath\$ … 入力ファイルのフォルダパス（最後に\はなし）（バッチのみ）
- \$InFileName\$ … 入力ファイル名（拡張子なし）（バッチのみ）
- \$OutFolderPath\$ … 出力ファイルのフォルダパス（最後に\はなし）（バッチのみ）
- \$OutFileName\$ … 出力ファイル名（拡張子なし）（バッチのみ）





#### 実行後のみで有効
Amatsukaze の環境変数と同じマクロ
- \$SUCCESS\$ … 成功=1,失敗=0
- \$ERROR_MESSAGE\$ … エラーメッセージ（成功時でも出る場合がある）
- \$IN_DURATION\$ … 入力ファイルの再生時間の秒トータル（30分なら1800）
- \$OUT_DURATION\$… 出力ファイルの再生時間の秒トータル（30分なら1800）
- \$LOGO_FILE\$ … ロゴファイルパス
- \$NUM_INCIDENT\$ … インシデント数
- \$JSON_PATH\$ … 出力JSONパス
- \$LOG_PATH\$ … ログファイルパス

AmatsukazeNotifier 独自マクロ
- \$CDSecs\$ … AmatsukazeがCMと判定してカットした秒数（小数点以下四捨五入）
- \$CDHH\$ … AmatsukazeがCMと判定してカットした時間の時間2桁固定
- \$CDH\$ … AmatsukazeがCMと判定してカットした時間の時間
- \$CDMM\$ … AmatsukazeがCMと判定してカットした時間の分2桁固定
- \$CDM\$ … AmatsukazeがCMと判定してカットした時間の分
- \$CDSS\$ … AmatsukazeがCMと判定してカットした時間の秒2桁固定
- \$CDS\$ … AmatsukazeがCMと判定してカットした時間の秒
- \$CutDur\$ … AmatsukazeがCMと判定したカットした時間(m分s秒 or s秒)
- \$IDHH\$ … 変換前の再生時間の時間2桁固定
- \$IDH\$ … 変換前の再生時間の時間
- \$IDMM\$ … 変換前の再生時間の分2桁固定
- \$IDM\$ … 変換前の再生時間の分
- \$IDSS\$ … 変換前の再生時間の秒2桁固定
- \$IDS\$ … 変換前の再生時間の秒
- \$ODHH\$ … 変換後の再生時間の時間2桁固定
- \$ODH\$ … 変換後の再生時間の時間
- \$ODMM\$ … 変換後の再生時間の分2桁固定
- \$ODM\$ … 変換後の再生時間の分
- \$ODSS\$ … 変換後の再生時間の秒2桁固定
- \$ODS\$ … 変換後の再生時間の秒
- \$InSizeByte\$ … 変換前のサイズ（バイト単位）
- \$InSizeKB\$ … 変換前のサイズ（KB単位）
- \$InSizeMB\$ … 変換前のサイズ（MB単位）
- \$InSizeGB\$ … 変換前のサイズ（GB単位）少数第一位まで
- \$OutSizeByte\$ … 変換後のサイズ（バイト単位）
- \$OutSizeKB\$ … 変換後のサイズ（KB単位）
- \$OutSizeMB\$ … 変換後のサイズ（MB単位）
- \$OutSizeGB\$ … 変換後のサイズ（GB単位）少数第一位まで
- \$CompressSizeByte\$ … エンコードで圧縮したサイズ（バイト単位）
- \$CompressSizeKB\$ … エンコードで圧縮したサイズ（KB単位）
- \$CompressSizeMB\$ … エンコードで圧縮したサイズ（MB単位）
- \$CompressSizeGB\$ … エンコードで圧縮したサイズ（GB単位）少数第一位まで

Python の辞書 (dict) 形式で格納しているので、改行を入れる場合は文字列内に \n と入力してください。文字列は + で連結できます。  


また、PostEncSuccess と PostEncFailed 用にエラーメッセージを設定できます。

Amatsukazeからエラーが出力された際には \[エラー: DRCSマッピングのない文字 127件] や \[エラー: キャンセルされました] の様な文字列をメッセージの最後に追加します。
エラーがなかった場合には追加されません。
このエラーメッセージも config.py の ErrorMessage でマクロで自由にカスタマイズする事が可能です。
エラーメッセージを使用しない場合は ErrorMessage = ''のように何も入力しないでください。

デフォルトのように絵文字も送信できます（ただ新しい絵文字だと端末側で表示できなかったりするので注意）。  
カスタマイズしたい方は、お好みの通知メッセージへ変更してみてください。

### 3. LINE Notify

LINE Notify へ通知しない場合は必要ありませんが、後述する Twitter の開発者アカウントを作成する手順よりもはるかに簡単なので、やっておくことをおすすめします（さほど手間もかかりません）。

[LINE Notify](https://notify-bot.line.me/ja/) にアクセスし、右上の \[ログイン] から LINE へログインします（いつも使っているアカウントで構いません）。  
ログインできたら、右上のメニューから \[マイページ] に移動します。

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/07.png)

下の方にある「アクセストークンの発行(開発者向け)」へ行き、 \[トークンを発行する] をクリックします。

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/08.png)

トークン名は LINE Notify で通知が送られてきたときに \[AmatsukazeNotifier] のように付加される文字列です（ LINE Notify 全体でユニークである必要はないらしい）。  
通知を送信するトークルームは \[1:1 で LINE Notify から通知を受ける] か、任意のグループ LINE を選択してください。  
ここでは「1:1 で LINE Notify から通知を受ける」（現在ログインしているアカウントに届く）を選択します。 

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/09.png)

 \[発行する] をクリックするとアクセストークンが発行されるので、 \[コピー] をクリックしてクリップボードにコピーします。  
アクセストークンはこの画面を閉じると二度と表示されない（一度解除し同じ内容でもう一度発行することはできるがアクセストークンは変わる）ので、どこかにメモしておくと良いでしょう。

![Screenshot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/10.png)

画面を閉じると LINE Notify と設定したトークルームが連携されているはずです。

最後に config.py を開き、先程クリップボードにコピーしたアクセストークンを \[LINE Notify] セクションの **LINE_ACCESS_TOKEN** に設定します。

これで、LINE Notify に通知を送信できる状態になりました！ 


### 4. Twitter (ツイート・ダイレクトメッセージ)

Twitter へ通知する場合は Twitter へ開発者登録を申請し、開発者アカウントを取得しておく必要があります（Twitter Developer アプリケーションの作成に Twitter の開発者アカウントが必要なため）。  
ただ、悪用する人が多かったため今から登録するのはちょっと面倒になっています。これでも最近若干緩和されたらしいけど…

さすがに手順までは説明しきれないので、開発者申請の手順が解説されている記事を貼っておきます（[記事1](https://digitalnavi.net/internet/3072/)・[記事2](https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/)）。  

すでにツイートさせたいアカウントとは別のアカウントで開発者アカウントになっている場合、必ずしも別途録画通知用の Bot アカウントを開発者アカウントにする必要はありません。  
Twitter API を使うためには後述する Consumer Key・Consumer Secret・Access Token・Access Token Secret の 4 つが必要ですが、このうち Twitter Developers でアプリ作成後に生成できる Access Token・Access Token Secret は開発者アカウントをしたアカウントのものが表示されます。  
裏を返せば、予め開発者アカウントで Consumer Key・Consumer Secret を作成・取得し、ツイートさせたい Twitter アカウントとアプリ連携して Access Token・Access Token Secret が取得できれば、開発者登録をしたアカウント以外でも録画通知用のアカウントにできる、とも言えます。

EDCBNotifierの作者tsukumijima氏のツールである、[Twitter API のアクセストークンを確認するやつ](https://tools.tsukumijima.net/twittertoken-viewer/) を使うと、AmatsukazeNotifier のようなアプリ連携を実装していないツールでも Access Token・Access Token Secret を取得できます（極論、これを使わなくても作成した Consumer Key・Consumer Secret で録画通知用のアカウントとアプリ連携して Access Token・Access Token Secret を取得できれば可能です）。  

[Twitter Developers](https://developer.twitter.com/en/apps) にアクセスし、右上の \[Create App] から Twitter Developer アプリケーションの作成画面に移動します（ここで言う Twitter Developer アプリケーション（以下 Twitter API アプリ）は Twitter API を使うプロジェクトのような意味です）。  
Twitter API アプリを作成すると、Twitter API を使うために必要な Consumer Key・Consumer Secret を取得できます。   
すでに Twitter API アプリを作成している場合は飛ばすこともできますが、via が被るので新しく作ってもいいと思います。開発者登録のときとは異なり、審査はありません。

![ScreenShot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/11.png)

#### App name（必須・重複不可らしい）

ここの名前がツイートの via として表示されます。  
いわゆる「独自 via 」と呼ばれるものです。後で変えることもできるので、好きな via にしましょう。

（例）AmatsukazeNotifier@（自分の TwitterID ）  
（例）Twitter for （自分の Twitter 名）  

#### Application description（必須）

（例）AmatsukazeNotifier@example から録画通知をツイートするためのアプリケーションです。

#### Website URL（必須）

利用用途的に自分以外は見ない部分なので、適当に設定しておきましょう。  
ただし、http://127.0.0.1/ は設定できないようです。

（例）https://example.com/  
（例）https://(自分のサイトのドメイン)/

#### Enable Sign in with Twitter

開発者登録をしたアカウント以外で利用する場合はチェックを入れてください。

#### Callback URLs

開発者登録をしたアカウント以外で利用する場合、アプリ連携をした後にリダイレクトされるコールバック URL を指定してください（複数設定できます）。  
[Twitter API のアクセストークンを確認するやつ](https://tools.tsukumijima.net/twittertoken-viewer/) を使う場合は `https://tools.tsukumijima.net/twittertoken-viewer/` を設定します。

#### Terms of service URL

無記入で OK です。

#### Privacy policy URL

無記入で OK です。

#### Organization name

無記入で OK です。

#### Organization website URL

無記入で OK です。

#### Tell us how this app will be used（必須）  

（例）このアプリケーションは、AmatsukazeNotifier から通知をツイートするためのアプリケーションです。  
　　　このアプリケーションは、テレビの録画予約の追加・変更、録画の開始・終了をツイートやダイレクトメッセージで通知します。

#### （英語・こちらをコピペ）

（例）This application is for tweeting notifications from AmatsukazeNotifier.   
　　　This application notifies you of the addition/change of TV recording reservation and the start/end of recording by tweet or directmessage.

記入し終えたら \[Create] をクリックし、Twitter API アプリを作成します。

ダイレクトメッセージを送信するため Permissions タブに移動し、\[Edit] をクリックします。

![ScreenShot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/12.png)

**Access permission** を **Read, write, and Direct Messages** に設定し、\[Save] で保存します。  
こうすることでツイートの読み取り・ツイートの書き込みなどに加え、ダイレクトメッセージを送信できるようになります。  
Permissions を変更すると今までに取得した Access Token・Access Token Secret が無効になります。注意してください。

![ScreenShot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/13.png)

Keys and tokens タブに移動し、API Key と API Key Secret をクリップボードにコピーします。  
API Key が Consumer Key 、API Key Secret が Consumer Secret にあたります。  

![ScreenShot](https://github.com/nukemiri/AmatsukazeNotifier/blob/images/Readme/14.png)

開発者登録したアカウントで利用する場合は、**Access token & access token secret** の横の \[Generate]をクリックし、Access Token・Access Token Secret を生成します。  
Access Token・Access Token Secret が表示されるので、クリップボードにコピーします。
このとき、Access Token・Access Token Secret は一度だけ表示されます。どこかにメモしておくとよいでしょう。  

開発者登録したアカウント以外で利用する場合は、自力でアプリ連携して Access Token・Access Token Secret を取得するか、録画通知用にしたいアカウントにログインした状態で [Twitter API のアクセストークンを確認するやつ](https://tools.tsukumijima.net/twittertoken-viewer/) に Consumer Key・Consumer Secret を入力し、Access Token・Access Token Secret をクリップボードにコピーしてください。

最後に config.py を開き、先程クリップボードにコピーしたアクセストークン等を \[Twitter API] セクションの **TWITTER_CONSUMER_KEY・TWITTER_CONSUMER_SECRET・TWITTER_ACCESS_TOKEN・TWITTER_ACCESS_TOKEN_SECRET** にそれぞれ設定します。

これで Twitter にツイートやダイレクトメッセージで通知を送信できる状態になりました！ 


これで設定は完了です！お疲れさまでした！   
なにか不具合や要望などあれば [Issues](https://github.com/nukemiri/AmatsukazeNotifier/issues) までお願いします。 

## License
[MIT Licence](LICENSE.txt)
