from src.models.entities.email import Email
from src.utils.utils import Utils
from src.models.dao.item import Item
from tabulate import tabulate


class Main:
    def __init__(self):
        parameters_json = Utils.retorna_parameters_json()
        item_instance = Item()

        itens = item_instance.get_codigo_itens
        precos = item_instance.get_prices_buff163(itens)

        valor_total_pago = item_instance.get_total_pago_itens
        item_instance.insert_historico_precos(precos)
        valor_total = item_instance.get_valor_total

        mensagem_email = f"""
                                {tabulate(item_instance.get_media_precos(),
                                          headers=['Item', 'Preço', 'Valor pago', 'Percentual', 'Quantidade', 'Valor total'],
                                          tablefmt='html',
                                          colalign=['left', 'left', 'left', 'left', 'center', 'left'])}
                                <br>
                                <b>Valor total dos itens:</b> R${valor_total}
                                <br>
                                <b>Valor total pago nos itens:</b> R${valor_total_pago}
                                <br>
                                <br>
                                <b>Lucro:</b> R${valor_total - valor_total_pago}
                            """

        Email.envia_email(remetente=parameters_json['email'][0]['endereco_remetente'],
                          destinatario=parameters_json['email'][0]['endereco_destinatario'],
                          senha=parameters_json['email'][0]['senha'],
                          titulo='Preço dos itens',
                          mensagem=mensagem_email)

        print('Email enviado com sucesso!')
        input('Digite qualquer tecla para sair...')


if __name__ == '__main__':
    Main()