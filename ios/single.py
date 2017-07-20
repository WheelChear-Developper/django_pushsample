import time
from apns import APNs, Payload

apns = APNs(use_sandbox=True, cert_file='develop.pem', key_file='secret.pem')

token_hex = '2b2cb83c5f430a76171bf605deda9cad1559a01956ebb07178280fc1752c886f'

content = "テスト!!"
content = content.decode('utf-8')

payload = Payload(alert=content, sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)