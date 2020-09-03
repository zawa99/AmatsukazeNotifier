import os
import sys
import colorama
import subprocess
import jaconv
import datetime
import config
import re

class Utils:

    def __init__(self):

        # 実行時刻
        self.time = datetime.datetime.now()

    def get_macro(self, environ):#環境変数を取得

        # 値が存在しなかった場合の初期値
        macro_default = '--'
        

        #tsファイルから番組情報を取得
        tsinfo = self.get_ts_info(environ.get("IN_PATH"))
        tsRecStart = tsinfo[0]
        tsDuration = tsinfo[1]
        tsRecEnd = tsinfo[2]
        
        

        #AmatsukazeがCMと判定してカットした秒数を取得
        InDurationSeconds = int('{:.0f}'.format(float(environ.get("IN_DURATION", "0"))))
        OutDurationSeconds = int('{:.0f}'.format(float(environ.get("OUT_DURATION", "0"))))
        CutDurationSeconds = int('{:.0f}'.format(float(environ.get("IN_DURATION", "0"))-float(environ.get("OUT_DURATION", "0"))))
        

        macro_table = {

            #追加時、実行前、実行後共通
            "ITEM_ID" : environ.get("ITEM_ID", macro_default), #アイテムに一意に振られるID。追加時、実行前、実行後で同じアイテムを追跡できる。Amatsukazeを再起動するとIDが変わるので注意。
            "IN_PATH" : environ.get("IN_PATH", macro_default), #入力ファイルパス
            "OUT_PATH" : environ.get("OUT_PATH", macro_default), #出力ファイルパス（拡張子を含まない）
            "SERVICE_ID" : environ.get("SERVICE_ID", macro_default), #サービスID（チャンネルID）
            "SERVICE_NAME" : environ.get("SERVICE_NAME", macro_default), #サービス名（チャンネル名）
            "TS_TIME" : environ.get("TS_TIME", macro_default), #TSファイルの時刻
            "ITEM_MODE" : environ.get("ITEM_MODE", macro_default), #モード。Batch:通常 AutoBatch:自動追加 Test:テスト DrcsCheck:DRCSチェック CMCheck:CMチェック
            "ITEM_PRIORITY" : environ.get("ITEM_PRIORITY", macro_default), #アイテム優先度(1-5)
            "ITEM_GENRE" : environ.get("ITEM_GENRE", macro_default), #番組ジャンル(
            "IMAGE_WIDTH" : environ.get("IMAGE_WIDTH", macro_default), #映像幅
            "IMAGE_HEIGHT" : environ.get("IMAGE_HEIGHT", macro_default), #映像高さ
            "EVENT_NAME" : environ.get("EVENT_NAME", macro_default), #番組名
            "TAG": environ.get("TAG", macro_default), #Amatsukazeで設定したタグ

            #実行前および実行後のみで有効
            "PROFILE_NAME": environ.get("PROFILE_NAME", macro_default), #プロファイル名

            #実行後のみで有効
            "SUCCESS": environ.get("SUCCESS", macro_default), #成功=1,失敗=0
            "ERROR_MESSAGE": environ.get("ERROR_MESSAGE", macro_default), #エラーメッセージ（失敗したときのみ）
            "IN_DURATION": environ.get("IN_DURATION", macro_default), #入力ファイルの再生時間
            "OUT_DURATION": environ.get("OUT_DURATION", macro_default), #出力ファイルの再生時間
            "IN_SIZE": environ.get("IN_SIZE", macro_default), #入力ファイルのサイズ（バイト単位）
            "OUT_SIZE": environ.get("OUT_SIZE", macro_default), #出力ファイルのサイズ（バイト単位）
            "LOGO_FILE": environ.get("LOGO_FILE", macro_default), #ロゴファイルパス
            "NUM_INCIDENT": environ.get("NUM_INCIDENT", macro_default), #インシデント数
            "JSON_PATH": environ.get("JSON_PATH", macro_default), #出力JSONパス
            "LOG_PATH": environ.get("LOG_PATH", macro_default), #ログファイルパス
            
            #独自マクロ
            "InFolderPath": os.path.dirname(environ.get("IN_PATH", macro_default)), #入力ファイルのフォルダパス（最後に\はなし）（バッチのみ）
            "InFileName": os.path.splitext(os.path.basename(environ.get("IN_PATH", macro_default)))[0], #入力ファイル名（拡張子なし）（バッチのみ）
            "OutFolderPath": os.path.dirname(environ.get("OUT_PATH", macro_default)), #出力ファイルのフォルダパス（最後に\はなし）（バッチのみ）
            "OutFileName": os.path.basename(environ.get("OUT_PATH", macro_default)), #出力ファイル名（拡張子なし）（バッチのみ）
            "Title": environ.get("EVENT_NAME", macro_default), #番組名
            "Title2": re.sub("\[.+?\]", "", environ.get("EVENT_NAME", macro_default)), #番組名（[]の括弧でくくられている部分を削除したもの）
            "SID10": environ.get("SERVICE_ID", macro_default), #ServiceID 10進数
            "SID16": hex(int(environ.get("SERVICE_ID", macro_default))), #ServiceID 16進数
            "ServiceName": environ.get("SERVICE_NAME", macro_default), #サービス名
            # Amatsukazeからジャンル情報が来ない事がある
            #"Genre": environ.get("ITEM_GENRE", macro_default).split(" - ")[0], #番組のジャンル
            #"Genre2": environ.get("ITEM_GENRE", macro_default).split(" - ")[len(environ.get("ITEM_GENRE", macro_default).split(" - "))-1], #番組の詳細ジャンル
            "Genre": tsinfo[4].replace("\u3000"," "), #ジャンル 〔詳細ジャンル〕,
            "SubTitle": tsinfo[3].replace("\u3000"," "), #サブタイトル
            
            "HashTag": self.get_hashtag(jaconv.z2h(environ.get('SERVICE_NAME', macro_default), digit = True, ascii = True, kana = False)), 
            "ServiceNameHankaku": jaconv.z2h(environ.get('SERVICE_NAME', macro_default), digit = True, ascii = True, kana = False), #サービス名（チャンネル名） 英数半角
            "TitleHankaku": jaconv.z2h(environ.get('EVENT_NAME', macro_default), digit = True, ascii = True, kana = False), #番組名 英数半角
            "Title2Hankaku": jaconv.z2h(re.sub("\[.+?\]", "", environ.get("EVENT_NAME", macro_default)), digit = True, ascii = True, kana = False), #番組名 英数半角
            "TimeYYYY": self.time.strftime("%Y"),
            "TimeYY": self.time.strftime("%y"),
            "TimeMM": self.time.strftime("%m"),
            "TimeM": str(int(self.time.strftime("%m"))),
            "TimeDD": self.time.strftime("%d"),
            "TimeD": str(int(self.time.strftime("%d"))),
            "TimeW": self.get_exection_day(),
            "TimeHH": self.time.strftime("%H"),
            "TimeH": str(int(self.time.strftime("%H"))),
            "TimeII": self.time.strftime("%M"),
            "TimeI": str(int(self.time.strftime("%M"))),
            "TimeSS": self.time.strftime("%S"),
            "TimeS": str(int(self.time.strftime("%S"))),
            
            
            
            "SDYYYY": tsRecStart.strftime("%Y"), #開始日の年4桁
            "SDYY": tsRecStart.strftime("%y"), #開始日の年2桁
            "SDMM": tsRecStart.strftime("%m"), #開始日の月2桁固定
            "SDM": str(int(tsRecStart.strftime("%m"))), #開始日の月
            "SDDD": tsRecStart.strftime("%d"), #開始日の日2桁固定
            "SDD": str(int(tsRecStart.strftime("%d"))), #開始日の日
            "SDW": self.get_weekday(tsRecStart), #開始日の曜日
            "STHH": tsRecStart.strftime("%H"), #開始時刻の時2桁固定
            "STH": str(int(tsRecStart.strftime("%H"))), #開始時刻の時
            "STMM": tsRecStart.strftime("%M"), #開始時刻の分2桁固定
            "STM": str(int(tsRecStart.strftime("%M"))), #開始時刻の分
            "STSS": tsRecStart.strftime("%S"), #開始時刻の秒2桁固定
            "STS": str(int(tsRecStart.strftime("%S"))), #開始時刻の秒
            "EDYYYY": tsRecEnd.strftime("%Y"), #終了日の年4桁
            "EDYY": tsRecEnd.strftime("%y"), #終了日の年2桁
            "EDYY": tsRecEnd.strftime("%y"), #終了日の年4桁
            "EDMM": tsRecEnd.strftime("%m"), #終了日の月2桁固定
            "EDM": str(int(tsRecEnd.strftime("%m"))), #終了日の月
            "EDDD": tsRecEnd.strftime("%d"), #終了日の日2桁固定
            "EDD": str(int(tsRecEnd.strftime("%d"))), #終了日の日
            "EDW": self.get_weekday(tsRecEnd), #終了日の曜日
            "ETHH": tsRecEnd.strftime("%H"), #終了時刻の時2桁固定
            "ETH": str(int(tsRecEnd.strftime("%H"))), #終了時刻の時
            "ETMM": tsRecEnd.strftime("%M"), #終了時刻の分2桁固定
            "ETM": str(int(tsRecEnd.strftime("%M"))), #終了時刻の分
            "ETSS": tsRecEnd.strftime("%S"), #終了時刻の秒2桁固定
            "ETS": str(int(tsRecEnd.strftime("%S"))), #終了時刻の秒
            "DUHH": str(self.Seconds_to_HMS(tsDuration.seconds)[1]).zfill(2), #番組総時間の時2桁固定（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            "DUH": str(self.Seconds_to_HMS(tsDuration.seconds)[1]), #番組総時間の時（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            "DUMM": str(self.Seconds_to_HMS(tsDuration.seconds)[2]).zfill(2), #番組総時間の分2桁固定（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            "DUM": str(self.Seconds_to_HMS(tsDuration.seconds)[2]), #番組総時間の分（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            "DUSS": str(self.Seconds_to_HMS(tsDuration.seconds)[3]).zfill(2), #番組総時間の秒2桁固定（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            "DUS": str(self.Seconds_to_HMS(tsDuration.seconds)[3]), #番組総時間の秒（ファイル名：録画開始時の番組総時間、Bat：録画終了時の番組総時間）
            
            #実行後のみ
            
            #AmatsukazeがCMと判定してカットした時間
            "CDSecs": str(CutDurationSeconds), #AmatsukazeがCMと判定してカットした秒数（小数点以下四捨五入）
            "CDHH": str(self.Seconds_to_HMS(CutDurationSeconds)[1]).zfill(2),
            "CDH": str(self.Seconds_to_HMS(CutDurationSeconds)[1]),
            "CDMM": str(self.Seconds_to_HMS(CutDurationSeconds)[2]).zfill(2),
            "CDM": str(self.Seconds_to_HMS(CutDurationSeconds)[2]),
            "CDSS": str(self.Seconds_to_HMS(CutDurationSeconds)[3]).zfill(2),
            "CDS": str(self.Seconds_to_HMS(CutDurationSeconds)[3]),
            "CutDur": self.Seconds_to_HMS(CutDurationSeconds)[0], #AmatsukazeがCMと判定したカットした時間(m分s秒 or s秒)
            
            #変換前の再生時間
            "IDHH": str(self.Seconds_to_HMS(InDurationSeconds)[1]).zfill(2),
            "IDH": str(self.Seconds_to_HMS(InDurationSeconds)[1]),
            "IDMM": str(self.Seconds_to_HMS(InDurationSeconds)[2]).zfill(2),
            "IDM": str(self.Seconds_to_HMS(InDurationSeconds)[2]),
            "IDSS": str(self.Seconds_to_HMS(InDurationSeconds)[3]).zfill(2),
            "IDS": str(self.Seconds_to_HMS(InDurationSeconds)[3]),
            
            #変換後の再生時間
            "ODHH": str(self.Seconds_to_HMS(OutDurationSeconds)[1]).zfill(2),
            "ODH": str(self.Seconds_to_HMS(OutDurationSeconds)[1]),
            "ODMM": str(self.Seconds_to_HMS(OutDurationSeconds)[2]).zfill(2),
            "ODM": str(self.Seconds_to_HMS(OutDurationSeconds)[2]),
            "ODSS": str(self.Seconds_to_HMS(OutDurationSeconds)[3]).zfill(2),
            "ODS": str(self.Seconds_to_HMS(OutDurationSeconds)[3]),

            "InSizeByte": str(int(environ.get("IN_SIZE", "0"))), #変換前のサイズ（バイト単位）
            "InSizeKB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")))/(1024))), #変換前のサイズ（KB単位）
            "InSizeMB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")))/(1024*1024))), #変換前のサイズ（MB単位）
            "InSizeGB": str('{:.1f}'.format((int(environ.get("IN_SIZE", "0")))/(1024*1024*1024))), #変換前のサイズ（GB単位）少数第一位まで
            "OutSizeByte": str(int(environ.get("IN_SIZE", "0"))), #変換後のサイズ（バイト単位）
            "OutSizeKB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")))/(1024))), #変換後のサイズ（KB単位）
            "OutSizeMB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")))/(1024*1024))), #変換後のサイズ（MB単位）
            "OutSizeGB": str('{:.1f}'.format((int(environ.get("IN_SIZE", "0")))/(1024*1024*1024))), #変換後のサイズ（GB単位）少数第一位まで
            "CompressSizeByte": str(int(environ.get("IN_SIZE", "0")) - int(environ.get("OUT_SIZE", "0"))), #エンコードで圧縮したサイズ（バイト単位）
            "CompressSizeKB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")) - int(environ.get("OUT_SIZE", "0")))/(1024))), #エンコードで圧縮したサイズ（KB単位）
            "CompressSizeMB": str('{:.0f}'.format((int(environ.get("IN_SIZE", "0")) - int(environ.get("OUT_SIZE", "0")))/(1024*1024))), #エンコードで圧縮したサイズ（MB単位）
            "CompressSizeGB": str('{:.1f}'.format((int(environ.get("IN_SIZE", "0")) - int(environ.get("OUT_SIZE", "0")))/(1024*1024*1024))) #エンコードで圧縮したサイズ（GB単位）少数第一位まで


        } 

        return macro_table

    # 放送局名からハッシュタグを取得する
    # BS-TBS が TBS と判定されるといったことがないよう BS・CS 局を先に判定する
    # service_name には半角に変換済みの放送局名が入るので注意
    # 参考: https://nyanshiba.com/blog/dtv-edcb-twitter
    def get_hashtag(self, service_name):

        # BS・CS

        if 'NHKBS1' in service_name:

            hashtag = '#nhkbs1'

        elif 'NHKBSプレミアム' in service_name:

            hashtag = '#nhkbsp'

        elif 'BS日テレ' in service_name:

            hashtag = '#bsntv'

        elif 'BS朝日' in service_name:

            hashtag = '#bsasahi'

        elif 'BS-TBS' in service_name:

            hashtag = '#bstbs'

        elif 'BSテレ東' in service_name:

            hashtag = '#bstvtokyo'

        elif 'BSフジ' in service_name:

            hashtag = '#bsfuji'

        elif 'BS11イレブン' in service_name:

            hashtag = '#bs11'

        elif 'BS12トゥエルビ' in service_name:

            hashtag = '#bs12'

        elif 'AT-X' in service_name:

            hashtag = '#at_x'

        # 地デジ
        
        elif 'NHK総合' in service_name:

            hashtag = '#nhk'

        elif 'NHKEテレ' in service_name:

            hashtag = '#etv'

        elif 'tvk' in service_name:

            hashtag = '#tvk'

        elif 'チバテレ' in service_name:

            hashtag = '#chibatv'

        elif '日テレ' in service_name:

            hashtag = '#ntv'

        elif 'テレビ朝日' in service_name:

            hashtag = '#tvasahi'

        elif 'TBS' in service_name:

            hashtag = '#tbs'

        elif 'テレビ東京' in service_name:

            hashtag = '#tvtokyo'

        elif 'フジテレビ' in service_name:

            hashtag = '#fujitv'

        elif 'TOKYO MX' in service_name:

            hashtag = '#tokyomx'

        else:

            # ハッシュタグが見つからないのでそのまま利用
            hashtag = '#' + service_name

        return hashtag
    
    # エラー出力
    def error(self, message):

        print('Error: ' + message, end = '\n\n')
        sys.exit(1)


    #TSファイルから番組情報の一部を取得
    def get_ts_info(self, ts_path,):
        #rplsinfoのパスを取得
        rplsinfo = os.path.join(os.getcwd(),"AmatsukazeNotifier","rplsinfo.exe")
        print("rplsinfo: "+rplsinfo)
        
        #時間情報を取得
        d = subprocess.run([rplsinfo, ts_path, "-d"], stdout=subprocess.PIPE)
        date = d.stdout.decode("shift-jis") #YYYY/MM/DD
        t = subprocess.run([rplsinfo, ts_path, "-t"], stdout=subprocess.PIPE)
        time = t.stdout.decode("shift-jis") #HH/MM/SS
        p = subprocess.run([rplsinfo, ts_path, "-p"], stdout=subprocess.PIPE)
        duration = p.stdout.decode("shift-jis") #HH/MM/SS
        
        i = subprocess.run([rplsinfo, ts_path, "-i"], stdout=subprocess.PIPE)
        info = i.stdout.decode("shift-jis").replace("\r\n","")
        
        g = subprocess.run([rplsinfo, ts_path, "-g"], stdout=subprocess.PIPE)
        genre = g.stdout.decode("shift-jis").replace("\r\n","")
        
        #datetime,timedelta型に変換
        RecStart = datetime.datetime.strptime((date.strip()+" "+time.strip()), '%Y/%m/%d %H:%M:%S')
        DurationTime = datetime.timedelta(hours=int(duration[:2]), minutes=int(duration[3:5]), seconds=int(duration[6:8]))
        RecEnd = RecStart + DurationTime
        

        #放送開始時刻(datetime)、放送時間(timedelta)、放送終了時刻(timedelta)、曜日リスト(list)を返す
        return RecStart, DurationTime, RecEnd, info, genre
        
        

    # 実行時刻
    def get_exection_time(self):
        return self.time


    # 実行曜日
    # 参考: https://note.nkmk.me/python-datetime-day-locale-function/
    def get_exection_day(self):
        weeklist = ['月', '火', '水', '木', '金', '土', '日']
        return weeklist[self.time.weekday()]


    # バージョン情報
    def get_version(self):

        return '1.0.0 alpha'

    #datetimeから曜日
    def get_weekday(self, in_datetime):
        weeklist = ['月', '火', '水', '木', '金', '土', '日']
        return weeklist[in_datetime.weekday()]
    
    # timedeltaから時間を取得
    def Seconds_to_HMS(self, totalseconds):
        if totalseconds>=3600: #1時間以上
            H = totalseconds//60
            M = (totalseconds%60)//60
            S = (totalseconds%60)%60
            timejp = str(H)+"時間"+str(M)+"分"+str(S)+"秒"
            
        elif totalseconds<60: #1分未満
            H = 0
            M = 0
            S = totalseconds
            timejp = str(S)+"秒"

        else: #1分以上1時間未満
            H = 0
            M = totalseconds//60
            S = totalseconds%60
            timejp = str(M)+"分"+str(S)+"秒"

        return timejp, H, M, S
