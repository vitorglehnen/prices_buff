from datetime import datetime
from tabulate import tabulate
import psycopg2 as db
import email.message
import pandas as pd
import requests
import smtplib


def conexao_db():
    parametros = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "postgres"}

    conexao = db.connect(**parametros)

    return conexao


def busca_preco_api(item):
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

    query.execute('''SELECT i.descricao "Item",
                    CONCAT('R$', ROUND(avg(hp.preco), 2)) "Média últimos 3 dias",
                    CONCAT('R$', i.precovendido) "Preço vendido",
                    CASE WHEN (i.precovendido > avg(hp.preco)) THEN CONCAT('+ ', ABS(ROUND(((avg(hp.preco) - i.precovendido) / i.precovendido) * 100, 2)), '%')
                    WHEN (i.precovendido < avg(hp.preco)) THEN CONCAT('- ', ABS(ROUND(((avg(hp.preco) - i.precovendido) / i.precovendido) * 100, 2)), '%')
                    end as "Percentual"
                    FROM historicoprecos hp
                    INNER JOIN item i on i.coditem = hp.coditem
                    WHERE hp.datacons BETWEEN (CURRENT_DATE - 3) and CURRENT_DATE
                    GROUP BY hp.coditem, i.coditem
                    ORDER BY ROUND(((avg(hp.preco) - i.precovendido) / i.precovendido) * 100, 2)''')

    result = query.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in query.description])

    query.close()
    conexao.close()

    return df


def envia_email(mensagem):
    msg = email.message.Message()

    msg['From'] = 'vitor.lehnen@universo.univates.br'
    msg['To'] = 'vitorlehnen.jojo@gmail.com'
    msg['Subject'] = 'Preços ' + str(datetime.now().date())

    senha = 'ecbzattdneovdoqj'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(mensagem)

    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()

    smtp.login(msg['From'], senha)
    smtp.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    smtp.quit()


lista_itens = []

for item in busca_tabela_item():
    preco_item = (list(item)[0], busca_preco_api(list(item)[0]))
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

string = tabulate(busca_media_precos(),
                  headers='keys',
                  tablefmt='html',
                  showindex=False,
                  stralign='left',
                  colalign=('left', ))

envia_email(string)
print("Email enviado!")
