
import os
import sys
import colorama
from ruamel.yaml import YAML
from pprint import pprint

from utils import Utils
from sendLine import Line
from sendDiscord import Discord

# 定数
VERSION = '1.0.2 beta'

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.yml')
LOG_FILE = os.path.join(BASE_DIR, 'AmatsukazeNotifier.log')

def load_config(config_path):
    """YAMLファイルから設定を読み込む"""
    if not os.path.exists(config_path):
        print('error: Config file not found.')
        sys.exit(1)

    with open(config_path, encoding='UTF-8') as stream:
        yaml = YAML()
        return yaml.load(stream)

def initialize_logging(config):
    """ログ出力先を設定"""
    if config['general'].get('notify_log'):
        sys.stdout = open(LOG_FILE, mode='w', encoding='utf-8')

def print_header(utils):
    """ヘッダー情報を出力"""
    header = '+' * 60
    version_info = f"AmatsukazeNotifier version {VERSION}"
    print(f"\n{header}\n+{version_info:^58}+\n{header}")
    print('Time: ' + str(utils.get_execution_time()) + '\n')

def get_notification_message(config, caller):
    """通知メッセージを取得"""
    if caller in config['message'] and caller in config['general']['notify_events']:
        return "\n".join(config['message'][caller])
    elif caller in config['message']:
        print(f'Info: {caller} notification is off, so it ends.')
        sys.exit(0)
    else:
        return None

def replace_macros(message, macros):
    """メッセージ内のマクロを置換"""
    for macro, macro_value in macros.items():
        message = message.replace(f'${macro}$', macro_value)
    return message

def get_notify_image(config):
    """通知用の画像を取得"""
    image_path = config['general'].get('notify_image')
    if image_path:
        full_path = os.path.join(os.path.dirname(__file__), image_path)
        if os.path.isfile(image_path):
            return image_path
        elif os.path.isfile(full_path):
            return full_path
    return None

def send_line_notification(config, message, image):
    """LINE Notifyを使って通知を送信"""
    if 'LINE' in config['general']['notify_types']:
        line = Line(config['line']['access_token'])
        try:
            result = line.send_message(message, image=image)
            if result['status'] == 200:
                print(f'[LINE Notify] Result: Success (Code: {result["status"]})')
                print(f'[LINE Notify] Message: {result["message"]}\n')
            else:
                print(f'[LINE Notify] Result: Failed (Code: {result["status"]})')
                print(f'[LINE Notify] {colorama.Fore.RED}Error: {result["message"]}\n')
        except Exception as error:
            print(f'[LINE Notify] Result: Failed')
            print(f'[LINE Notify] {colorama.Fore.RED}Error: {error}\n')

def send_discord_notification(config, message, image):
    """Discord Webhookを使って通知を送信"""
    if 'Discord' in config['general']['notify_types']:
        discord = Discord(config['discord']['webhook_url'])
        try:
            result = discord.send_message(message, image=image)
            if result['status'] in {200, 204}:
                print(f'[Discord] Result: Success (Code: {result["status"]})')
                print(f'[Discord] Message: {result["message"]}\n')
            else:
                print(f'[Discord] Result: Failed (Code: {result["status"]})')
                print(f'[Discord] {colorama.Fore.RED}Error: {result["message"]}\n')
        except Exception as error:
            print(f'[Discord] Result: Failed')
            print(f'[Discord] {colorama.Fore.RED}Error: {error}\n')

def main():
    # 初期化
    colorama.init(autoreset=True)
    utils = Utils()

    # 設定ファイルの読み込み
    config = load_config(CONFIG_FILE)

    # ログ出力先の設定
    initialize_logging(config)

    # ヘッダー出力
    print_header(utils)

    # 引数確認
    if len(sys.argv) <= 1:
        utils.error('Argument does not exist.')
    caller = sys.argv[1]
    print(f'Event: {caller}\n')

    # 通知メッセージの取得
    message = get_notification_message(config, caller)
    if not message:
        utils.error('Invalid argument.')

    # マクロ置換
    macros = utils.get_macro(os.environ)
    message = replace_macros(message, macros)

    # エラーメッセージを追加
    errormessage = replace_macros("\n".join(config['error_message']), macros)
    if caller in ["PostEncSuccess", "PostEncFailed"] and macros.get("ERROR_MESSAGE"):
        message += f"\n{errormessage}"
        print("エラーメッセージを検出: " + errormessage)

    # 画像の取得
    image = get_notify_image(config)

    # 絵文字を無視してコンソールに出力
    print(("Message: " + message.replace("\n", "\n                 "))
          .encode('cp932', 'ignore').decode("cp932"), end="\n\n")

    # LINE通知の送信
    send_line_notification(config, message, image)
    # Discord通知の送信
    send_discord_notification(config, message, image)

if __name__ == '__main__':
    main()
