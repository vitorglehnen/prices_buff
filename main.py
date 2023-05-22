import requests
import psycopg2 as db
from datetime import datetime


def conexao_db():
    parametros = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "postgres"}

    conexao = db.connect(**parametros)

    return conexao


def busca_preco(item):
    api = requests.get(
        f'https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={item}&page_num=1').json()

    for price in api['data']['items']:
        return float(price['price'])


def busca_tabela_item():
    conexao = conexao_db()
    query = conexao.cursor()

    query.execute('SELECT coditem FROM item')
    result = query.fetchall()

    query.close()
    conexao.close()

    return result


def busca_media_precos():
    conexao = conexao_db()
    query = conexao.cursor()

    query.execute('SELECT coditem FROM item')
    result = query.fetchall()

    query.close()
    conexao.close()

    return result


lista_itens = []

for item in busca_tabela_item():
    preco_item = (list(item)[0], busca_preco(list(item)[0]))
    lista_itens.append(preco_item)

for coditem, preco in lista_itens:
    data_agora = str(datetime.now().date().strftime('%d/%m/%Y'))
    hora_agora = str(datetime.now().time().strftime('%H:%M:%S'))

    conexao = conexao_db()
    query = conexao.cursor()

    query.execute(f"INSERT INTO historicoprecos(controle, coditem, preco, datacons, horacons)"
                  f"VALUES (nextval('gen_controle_histprecos'), {coditem}, {preco}, '{data_agora}', '{hora_agora}')")

    conexao.commit()
    query.close()
    conexao.close()
