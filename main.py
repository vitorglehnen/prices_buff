from src.models.item import Item
from src.models.bitcoin import Bitcoin
from src.models.email import Email
from src.utils.utils import Utils
from tabulate import tabulate

import json


Utils.cria_parameters_json()

with open('parameters.json', 'r') as file:
    parameters_email = json.load(file)

item_instance = Item()

itens = item_instance.get_codigo_itens
precos = item_instance.get_prices_buff163(itens)
preco_bitcoin = Bitcoin.get_price()
valor_total = item_instance.get_valor_total

item_instance.insert_historico_precos(precos)

mensagem_email = f"""
                    {tabulate(item_instance.get_media_precos(), headers=['Item', 'Preço', 'Valor pago', 'Percentual', 'Quantidade', 'Valor total'], tablefmt='html', colalign=['left', 'left', 'left', 'left', 'center', 'left'])}
                    <br>
                    <b>Valor total dos itens:</b> R${valor_total}
                    <br>     
                    <b>Preço do bitcoin:</b> R${preco_bitcoin}                
                    """

Email.envia_email(remetente=parameters_email['email'][0]['endereco_remetente'],
                  destinatario=parameters_email['email'][0]['endereco_destinatario'],
                  senha=parameters_email['email'][0]['senha'],
                  titulo='Preço dos itens',
                  mensagem=mensagem_email)
