
# ====================  環境設定  ====================

# [] で囲われている部分は配列 (list)
# {} で囲われている部分は辞書 (dict)
# 文字列は必ずシングルクオート ('') で囲んでください
# ハッシュ (#) をつけるとコメントになります (// はコメントにならない)
# 文字コード UTF-8 (BOM なし)・改行コード LF 以外で保存すると動作しなくなるので注意（メモ帳は基本的に NG）
# できれば VSCode などのシンタックスハイライトのあるエディタでの編集を推奨します


# 通知タイプ
# LINE (LINE Notify)・Tweet (ツイート)・DirectMessage (ダイレクトメッセージ) から設定
# [] 内にカンマ区切りで複数設定できます

# ex (LINE): NOTIFY_TYPE = ['LINE']
# ex (ツイート): NOTIFY_TYPE = ['Tweet']
# ex (ダイレクトメッセージ): NOTIFY_TYPE = ['DirectMessage']
# ex (LINE とツイート): NOTIFY_TYPE = ['LINE', 'Tweet']
# ex (LINE とダイレクトメッセージ): NOTIFY_TYPE = ['LINE', 'DirectMessage']
# ex (全て): NOTIFY_TYPE = ['LINE', 'Tweet', 'DirectMessage']

NOTIFY_TYPE = ['LINE', 'Tweet', 'DirectMessage']


# 通知を行うイベント
# 通知イベントのオン・オフを指定できます（たとえば頻度の多い PostNotify だけ通知しない設定も可能）
# ここで設定したイベントだけが通知されます（通知オフ） 設定されなかったイベントは通知されない（通知オフ）
# 各 .bat ファイルを配置しないことでも通知イベントのオン・オフは可能ですが、できるだけこの設定を使うことを推奨します

# PostEncStart … 変換を開始したとき
# PostEncSuccess … 変換が成功したとき
# PostEncFailed … 変換が失敗したとき

# ex (全て通知): NOTIFY_EVENT = ['PostEncStart', 'PostEncSuccess', 'PostEncFailed']
# ex (変換終了時のみ通知): NOTIFY_EVENT = ['PostEncSuccess', 'PostEncFailed']

NOTIFY_EVENT = ['PostEncStart', 'PostEncSuccess', 'PostEncFailed']


# 通知時に同時に送信する画像 (フルパスで指定)
# 画像を config.py と同じ階層に置く場合はファイル名だけの指定でも OK
# 画像サイズが大きすぎると送れない場合があるので注意
# None (シングルクオートはつけない) に設定した場合は画像を送信しません

# ex: NOTIFY_IMAGE = 'C:\Users\User\Pictures\AmatsukazeNotifier.png'
# ex: NOTIFY_IMAGE = 'AmatsukazeNotifier.png'
# ex: NOTIFY_IMAGE = None

NOTIFY_IMAGE = None


# ダイレクトメッセージの宛先 (スクリーンネーム (@ から始まる ID) で指定)
# 上の設定で DirectMessage (ダイレクトメッセージ) を設定した場合に適用されます
# @ はつけずに指定してください 予め宛先のアカウントと DM が送信できる状態になっていないと送れません
# None (シングルクオートはつけない) に設定した場合は自分宛てに送信します

# ex: NOTIFY_DIRECTMESSAGE_TO = 'AbeShinzo'
# ex: NOTIFY_DIRECTMESSAGE_TO = None

NOTIFY_DIRECTMESSAGE_TO = None


# ログをファイルに保存（出力）するか
# True に設定した場合は、ログを config.py と同じフォルダの EDCBNotifier.log に保存します（コンソールに表示しない・前回のログは上書きされる）
# False に設定した場合は、ログを保存しません（コンソールに表示する）
# True・False にはシングルクオートをつけず、大文字で始めてください (true・false は NG)
# うまく通知されないときに True にしてログを確認してみるといいかも

NOTIFY_LOG = False




# ===================  メッセージ  ===================

# 改行を入れる場合は文字列内に \n と入力してください
# 文字列は + で連結できます
#
# 使用可能なマクロについてはREADME.mdを参照

NOTIFY_MESSAGE = {

    # 変換を開始したとき（ 実行前_AmatsukazeNotifier.bat が実行されたとき）に送信するメッセージ
    'PostEncStart': '🔥 変換開始: $SDYYYY$/$SDMM$/$SDDD$($SDW$) $ServiceNameHankaku$ $HashTag$ \n' + '$STHH$:$STMM$～$ETHH$:$ETMM$ $TitleHankaku$\n'+'プロファイル: $PROFILE_NAME$',

    # 変換が成功したとき（ 実行後_AmatsukazeNotifier.bat が実行されたとき）に送信するメッセージ
    'PostEncSuccess': '✅ 変換成功: $SDYYYY$/$SDMM$/$SDDD$($SDW$) $ServiceNameHankaku$ $HashTag$ \n' + '$STHH$:$STMM$～$ETHH$:$ETMM$ $TitleHankaku$\n'+'プロファイル: $PROFILE_NAME$\n'+'カット: $CutDur$ 圧縮: $CompressSizeGB$GB',
    
    # 変換が失敗したとき（ 実行後_AmatsukazeNotifier.bat が実行されたとき）に送信するメッセージ
    'PostEncFailed': '⚠️ 変換失敗: $SDYYYY$/$SDMM$/$SDDD$($SDW$) $ServiceNameHankaku$ $HashTag$ \n' + '$STHH$:$STMM$～$ETHH$:$ETMM$ $TitleHankaku$\n'+'プロファイル: $PROFILE_NAME$'
    

}

#変換終了時のエラーメッセージ

#PostEncSuccessまたはPostEncFailedではエラーメッセージがメッセージの下に追加されます
#エラーがない場合にはエラーメッセージは追加されません
#エラーメッセージにもマクロを使用する事ができます
#エラーメッセージを表示したくない場合は ErrorMessage = ''　の用にクオーテーション内を空欄にしてください。

ErrorMessage = 'エラー: $ERROR_MESSAGE$'

# ==================  LINE Notify  ==================

# LINE Notify のアクセストークン
LINE_ACCESS_TOKEN = 'YOUR_LINE_ACCESS_TOKEN'


# ==================  Twitter API  ==================

# Twitter API のコンシューマーキー
TWITTER_CONSUMER_KEY = 'YOUR_TWITTER_CONSUMER_KEY'

# Twitter API のコンシューマーシークレット
TWITTER_CONSUMER_SECRET = 'YOUR_TWITTER_CONSUMER_SECRET'

# Twitter API のアクセストークン
TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'

# Twitter API のアクセストークンシークレット
TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
