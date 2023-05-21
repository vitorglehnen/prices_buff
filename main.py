import requests
import time
import psycopg2 as db


def conexao_db():
    parametros = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "postgres"}
    conexao = db.connect(**parametros)
    cursor = conexao.cursor()
    return cursor


def busca_preco(item):
    api = requests.get(
        f'https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={item}&page_num=1').json()

    for price in api['data']['items']:
        return float(price['price'])


query = conexao_db()
query.execute('SELECT coditem FROM item')
result = query.fetchall()

for item in result:
    lista_itens = list(item)
    print(busca_preco(lista_itens[0]))



