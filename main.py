import requests
from twilio.rest import Client

cloud9 = {'nome': 'CLOUD9', 'id': '894316', 'preco_vendido': 137.76}
furia = {'nome': 'FURIA', 'id': '894182', 'preco_vendido': 67.26}
copenhagen = {'nome': 'COPENHAGEN', 'id': '894390', 'preco_vendido': 29.44}
navi = {'nome': 'NAVI', 'id': '894280', 'preco_vendido': 38.40}
faze = {'nome': 'FAZE', 'id': '894178', 'preco_vendido': 37.70}
heroic = {'nome': 'HEROIC', 'id': '894259', 'preco_vendido': 25.44}
complexity = {'nome': 'COMPLEXITY', 'id': '894353', 'preco_vendido': 60.93}
liquid = {'nome': 'LIQUID', 'id': '895343', 'preco_vendido': 50.21}
noveZ = {'nome': '9ZTEAM', 'id': '894383', 'preco_vendido': 49.53}
big = {'nome': 'BIG', 'id': '894131', 'preco_vendido': 7.31}


def busca_preco(item):
    api = requests.get(f'https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={item["id"]}&page_num=1').json()

    for price in api['data']['items']:
        return float(price['price'])


def calcula_preco(valor_atual, item):
    if item['preco_vendido'] >= valor_atual:
        porcentagem = float(valor_atual) / item['preco_vendido'] * 100
        texto = f'{item["nome"]} - \nProfit: +{round(100 - porcentagem, 2)}%, \nValor atual: {valor_atual}, \nValor vendido: {item["preco_vendido"]}'
        return texto
    elif item['preco_vendido'] <= float(valor_atual):
        porcentagem = item['preco_vendido'] / float(valor_atual) * 100
        texto = f'{item["nome"]} - \nDeficit: -{round(100 - porcentagem, 1)}%, \nValor atual: {valor_atual}, \nValor vendido: {item["preco_vendido"]}'
        return texto

mensagem = f'\n{calcula_preco(busca_preco(cloud9), cloud9)}\n\n' \
           f'{calcula_preco(busca_preco(furia), furia)}\n\n' \
           f'{calcula_preco(busca_preco(copenhagen), copenhagen)}\n\n' \
           f'{calcula_preco(busca_preco(navi), navi)}\n\n' \
           f'{calcula_preco(busca_preco(faze), faze)}\n\n' \
           f'{calcula_preco(busca_preco(heroic), heroic)}\n\n' \
           f'{calcula_preco(busca_preco(complexity), complexity)}\n\n' \
           f'{calcula_preco(busca_preco(liquid), liquid)}\n\n' \
           f'{calcula_preco(busca_preco(noveZ), noveZ)}\n\n' \
           f'{calcula_preco(busca_preco(big), big)}\n\n'

client = Client('AC9dd5dc6db412571cdf9f3e1706aa5ad3', 'b6e667dacfc8fbd9506142438f47cdb1')

message = client.messages.create(
    body= mensagem,
    from_= '+1 607 689 9924',
    to= '+5551992736586'
)






