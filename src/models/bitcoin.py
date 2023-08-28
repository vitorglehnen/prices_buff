import requests


class Bitcoin:

    @staticmethod
    def get_price():
        request = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl').json()

        return request['bitcoin']['brl']