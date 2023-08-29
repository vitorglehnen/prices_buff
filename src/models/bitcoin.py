from src.utils.utils import *
import requests


class Bitcoin:

    @staticmethod
    def get_price():
        try:
            request = requests.get('htt://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl').json()
            return request['bitcoin']['brl']
        except Exception as e:
            Utils.gera_log_erro("Erro ao buscar o preço do bitcoin! Log gerado em: ", str(e), sys._getframe().f_code.co_name)