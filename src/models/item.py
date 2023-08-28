from src.connection.connect import Connection
import requests


class Item:
    def __init__(self):
        conexao_instance = Connection()

        self.conexao = conexao_instance.conexao_db()
        self.query = self.conexao.cursor()

    @property
    def get_codigo_itens(self):
        sql = """
        
        SELECT coditem FROM item WHERE inativo = 'N'
        
        """

        self.query.execute(sql)
        result = self.query.fetchall()

        itens = []
        for item in result:
            itens.append(item[0])

        return itens

    @staticmethod
    def get_prices_buff163(itens):
        prices = {}

        for item in itens:
            request = requests.get(
                f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1691347901651").json()

            prices[item] = request['data']['items'][0]['price']

        return prices

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

        self.query.execute(sql)

        result = self.query.fetchone()

        return result[0]

    def insert_historico_precos(self, itens):
        for coditem, preco in itens.items():
            sql = f"""

                    INSERT INTO historicoprecos(controle, coditem, preco)
                    VALUES (nextval('gen_controle_histprecos'), {coditem}, {preco})

                    """

            self.query.execute(sql)

        self.conexao.commit()

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

        self.query.execute(sql)

        result = self.query.fetchall()

        return result

    @property
    def get_total_pago_itens(self):
        sql = f"""
                
                SELECT SUM(valor) AS valor_total
                FROM (SELECT (i.quantidade*preco) AS valor
                        FROM item i
                        WHERE i.inativo = 'N') SUB
                
                """

        self.query.execute(sql)

        result = self.query.fetchone()

        return result[0]

