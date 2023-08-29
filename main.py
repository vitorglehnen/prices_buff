from src.models.item import Item
from src.models.bitcoin import Bitcoin
from src.models.email import Email
from src.utils.utils import Utils
from tabulate import tabulate


class Main:
    def __init__(self):
        self.parameters_json = Utils.retorna_parameters_json()

        self.item_instance = Item()
        self.itens = self.item_instance.get_codigo_itens
        self.precos = self.item_instance.get_prices_buff163(self.itens)

        self.preco_bitcoin = Bitcoin.get_price()
        self.valor_total_pago = self.item_instance.get_total_pago_itens
        self.valor_total = self.item_instance.get_valor_total

        self.item_instance.insert_historico_precos(self.precos)

        self.mensagem_email = f"""
                                {tabulate(self.item_instance.get_media_precos(),
                                          headers=['Item', 'Preço', 'Valor pago', 'Percentual', 'Quantidade', 'Valor total'],
                                          tablefmt='html',
                                          colalign=['left', 'left', 'left', 'left', 'center', 'left'])}
                                <br>
                                <b>Valor total dos itens:</b> R${self.valor_total}
                                <br>
                                <b>Valor total pago nos itens:</b> R${self.valor_total_pago}
                                <br>
                                <br>
                                <b>Lucro:</b> R${self.valor_total - self.valor_total_pago}
                                <br>     
                                <br>
                                <b>Preço do bitcoin:</b> R${self.preco_bitcoin} 
                            """

        Email.envia_email(remetente=self.parameters_json['email'][0]['endereco_remetente'],
                          destinatario=self.parameters_json['email'][0]['endereco_destinatario'],
                          senha=self.parameters_json['email'][0]['senha'],
                          titulo='Preço dos itens',
                          mensagem=self.mensagem_email)

        print('Email enviado com sucesso!')
        input('Digite qualquer tecla para sair...')


if __name__ == '__main__':
    Main()