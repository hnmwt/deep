import requests
# lineチャットボット
def Line_bot(message):
    line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
    line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
