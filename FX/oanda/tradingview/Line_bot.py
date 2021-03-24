import requests
import backtest_variable
# lineチャットボット
def Line_bot(message):
    if backtest_variable.Line_bot == True:  # フラグがtrueの時
        line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
        line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)

def Line_bot_error(message):
    line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
    line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)