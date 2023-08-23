from datetime import datetime
from tabulate import tabulate
import pandas as pd
import requests
import emails
import params


def busca_preco_api(item):
    api = requests.get(
        f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1691347901651').json()

    for price in api['data']['items']:
        return float(price['price'])


def busca_tabela_item():
    conexao = params.conexao_db()
    query = conexao.cursor()

    query.execute('SELECT coditem FROM item')
    result = query.fetchall()

    query.close()
    conexao.close()

    return result


def busca_valor_total():
    conexao = params.conexao_db()
    query = conexao.cursor()

    query.execute(f'''select sum(valor_total)
                    from (select i.quantidade * max(h.preco) as valor_total
    	            from item i 
    	            inner join historicoprecos h on h.coditem = i.coditem and h.datacons = CURRENT_DATE
    	            group by h.coditem,i.coditem) sub''')

    valor_total = query.fetchone()
    query.close()
    conexao.close()

    return valor_total


def busca_media_precos():
    conexao = params.conexao_db()
    query = conexao.cursor()

    query.execute(f'''
        SELECT 
            i.descricao "Item",
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
       GROUP BY hp.coditem, i.coditem
       ORDER BY ROUND(((max(hp.preco) - i.preco) / i.preco) * 100, 2) DESC
        ''')

    result = query.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in query.description])
    query.close()
    conexao.close()

    return df


def busca_valor_bitcoin():
    req_bitcoin = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl').json()
    print()

    return req_bitcoin['bitcoin']['brl']


lista_itens = []

for item in busca_tabela_item():
    preco_item = (list(item)[0], busca_preco_api(list(item)[0]))
    lista_itens.append(preco_item)

for coditem, preco in lista_itens:
    data_agora = str(datetime.now().date().strftime('%d/%m/%Y'))
    hora_agora = str(datetime.now().time().strftime('%H:%M:%S'))

    conexao = params.conexao_db()
    query = conexao.cursor()

    query.execute(f"INSERT INTO historicoprecos(controle, coditem, preco)"
                  f"VALUES (nextval('gen_controle_histprecos'), {coditem}, {preco})")

    conexao.commit()
    query.close()
    conexao.close()

string = tabulate(busca_media_precos(),
                  headers='keys',
                  tablefmt='html',
                  showindex=False,
                  stralign='left',
                  colalign=('left',))

emails.envia_email('Preços do dia: ' + str(datetime.now().date()),
                    (string + '\n\n' + 'Valor total: R$' + str(busca_valor_total()[0]) + '\n\n' + 'Valor bitcoin: R$' + str(busca_valor_bitcoin())))

print("Email enviado!")
