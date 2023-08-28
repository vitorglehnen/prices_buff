from src.models.item import Item
from src.models.bitcoin import Bitcoin
from src.models.email import Email
from src.utils.utils import Utils
from tabulate import tabulate


parameters_email = Utils.retorna_parameters_json()

item_instance = Item()

itens = item_instance.get_codigo_itens
precos = item_instance.get_prices_buff163(itens)

preco_bitcoin = Bitcoin.get_price()
valor_total_pago = item_instance.get_total_pago_itens
valor_total = item_instance.get_valor_total

item_instance.insert_historico_precos(precos)

mensagem_email = f"""
                    {tabulate(item_instance.get_media_precos(), headers=['Item', 'Preço', 'Valor pago', 'Percentual', 'Quantidade', 'Valor total'], tablefmt='html', colalign=['left', 'left', 'left', 'left', 'center', 'left'])}
                    <br>
                    <b>Valor total dos itens:</b> R${valor_total}
                    <br>
                    <b>Valor total pago nos itens:</b> R${valor_total_pago}
                    <br>
                    <br>
                    <b>Lucro:</b> R${valor_total - valor_total_pago}
                    <br>     
                    <br>
                    <b>Preço do bitcoin:</b> R${preco_bitcoin} 
                    """

Email.envia_email(remetente=parameters_email['email'][0]['endereco_remetente'],
                  destinatario=parameters_email['email'][0]['endereco_destinatario'],
                  senha=parameters_email['email'][0]['senha'],
                  titulo='Preço dos itens',
                  mensagem=mensagem_email)
