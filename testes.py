import requests

req_bitcoin = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl').json()
print(float(req_bitcoin['bitcoin']['brl']))
