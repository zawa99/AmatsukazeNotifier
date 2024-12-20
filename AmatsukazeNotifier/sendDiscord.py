
import io
import json
import os
import requests


class Discord:
    """
    Discord の Webhook でメッセージを送信するクラス
    """

    def __init__(self, webhook_url:str):
        """
        Args:
            webhook_url (str): Discord の Webhook の URL
        """

        self.webhook_url = webhook_url


    def send_message(self, message:str, image = None) -> dict:
        """
        Discord の Webhook でメッセージを送信する

        Args:
            message (str): 送信するメッセージの本文
            image (str, optional): 送信する画像のファイルパス. Defaults to None.

        Returns:
            dict: ステータスコードとエラーメッセージが入った辞書
        """

        # 画像も送信する
        if image is not None and os.path.isfile(image):

            # メッセージ
            # ref: https://discord.com/developers/docs/reference#uploading-files
            payload = {
                'username':'AmatsukazeNotifier',
                'content': message,
                'attachments': [{
                    'id': 0,
                    'filename': os.path.basename(image),
                }]
            }

            # 送信するファイル
            # ref: https://qiita.com/bgcanary/items/6d81b7813434978362f4
            files = {
                'payload_json': ('', io.BytesIO(json.dumps(payload).encode('utf-8')), 'application/json'),
                'files[0]': (os.path.basename(image), open(image, 'rb')),
            }

            # Webhook を送信
            # 公式ドキュメントいわく、画像も一緒に送る場合は multipart/form-data である必要があるらしい
            # ref: https://discord.com/developers/docs/resources/webhook#execute-webhook
            response = requests.post(self.webhook_url, files=files)

        # テキストのみ
        else:

            # メッセージ
            payload = {
                'username':'AmatsukazeNotifier',
                'content': message,
            }

            # Webhook を送信
            response = requests.post(self.webhook_url, json=payload)

        # 失敗した場合はエラーメッセージを取得
        if response.status_code != 200 and response.status_code != 204:
            message = response.json()['message'] + f' (Code: {response.json()["code"]})'
        else:
            message = 'Success'

        # ステータスコードとエラーメッセージを返す
        return {
            'status': response.status_code,
            'message': message,
        }
