from src.connection.connect import Connection
from src.utils.utils import *
import requests

class Item:
    def __init__(self):
        self.conexao_instance = Connection()

    # Retorna uma lista de códigos de itens ativos
    @property
    def get_codigo_itens(self):
        sql = """
        SELECT coditem FROM item WHERE inativo = 'N'
        """
        result = self.conexao_instance.query_select(sql)
        itens = [item[0] for item in result]
        return itens

    # Retorna o valor total pago por todos os itens ativos
    @property
    def get_total_pago_itens(self):
        sql = f""" 
        SELECT SUM(valor) AS valor_total
        FROM (SELECT (i.quantidade * preco) AS valor
                FROM item i
                WHERE i.inativo = 'N') SUB
        """
        return self.conexao_instance.query_select(sql)[0][0]

    # Retorna o valor total dos itens da última consulta dos preços
    @property
    def get_valor_total(self):
        sql = """
        SELECT sum(valor_total)
        FROM (SELECT i.quantidade * MAX(h.preco) as valor_total
                FROM item i 
                JOIN historicoprecos h on h.coditem = i.coditem AND 
                                        h.datacons = CURRENT_DATE AND 
                                        h.horacons = (SELECT max(horacons)
                                                    FROM historicoprecos h2
                                                    WHERE h2.datacons = CURRENT_DATE AND 
                                                        h2.coditem = i.coditem)
                WHERE i.inativo = 'N'                                                        
                GROUP BY h.coditem,i.coditem) SUB
        """
        return self.conexao_instance.query_select(sql)[0][0]

    # Retorna os preços dos itens de uma API externa (buff.163)
    @staticmethod
    def get_prices_buff163(itens):
        prices = {}
        for item in itens:
            try:
                request = requests.get(
                    f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1691347901651'
                ).json()
                prices[item] = request['data']['items'][0]['price']
            except Exception as e:
                Utils.gera_log_erro("Erro ao consultar a API do buff163! Log gerado em: ", str(e), sys._getframe().f_code.co_name)
        return prices

    # Insere os preços dos itens no banco de dados
    def insert_historico_precos(self, itens):
        for coditem, preco in itens.items():
            sql = f"""
                    INSERT INTO historicoprecos(controle, coditem, preco)
                    VALUES (nextval('gen_controle_histprecos'), {coditem}, {preco})
                    """
            self.conexao_instance.query_insert(sql)

    # Retorna a média de preços de hoje dos itens ativos
    def get_media_precos(self):
        sql = f"""
        SELECT i.descricao "Item",
                CONCAT('R$', max(hp.preco)) "Preço hoje",
                CONCAT('R$', i.preco) "Preço comprado",
                COALESCE((CASE WHEN (i.preco > max(hp.preco)) THEN CONCAT('- ', ABS(ROUND(((max(hp.preco) - i.preco) / i.preco) * 100, 2)), '%')
                        WHEN (i.preco < max(hp.preco)) THEN CONCAT('+ ', ABS(ROUND(((max(hp.preco) - i.preco) / i.preco) * 100, 2)), '%')
                        END), '   0.00%') "Percentual",
                i.quantidade "Qtde",
                'R$' || (i.quantidade * max(hp.preco)) "Valor total"
        FROM historicoprecos hp
        INNER JOIN item i on i.coditem = hp.coditem
        WHERE hp.datacons = CURRENT_DATE and hp.horacons = (SELECT max(hp1.horacons) 
                                                            FROM historicoprecos hp1
                                                            WHERE hp1.datacons = CURRENT_DATE and
                                                            hp1.coditem = hp.coditem)
            AND i.inativo = 'N'                                                            
        GROUP BY hp.coditem, i.coditem
        ORDER BY ROUND(((max(hp.preco) - i.preco) / i.preco) * 100, 2) DESC
        """
        return self.conexao_instance.query_select(sql)
