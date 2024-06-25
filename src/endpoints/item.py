from flask import jsonify, request, Blueprint, make_response
from src.models.dao.item import ItemDao
from src.models.entities.item import Item

item_dao = ItemDao()
item = Blueprint('item', __name__)


@item.route('/itens/inserir', methods=['POST'])
def itens_inserir():
    item = Item(request.json['codigo'], request.json['descricao'], request.json['preco'], request.json['quantidade'], request.json['inativo'])

    item_dao.inserir(item)

    return jsonify('Item inserido com sucesso!')


@item.route('/itens/consultar/<codigo>', methods=['GET'])
def busca_item(codigo):
    item = Item(codigo, None, None, None, None)

    item_return = item_dao.buscar(item)

    if item_return.codigo is None:
        return jsonify("Código de produto inexistente na base de dados!")

    response = {
        'produtos': [{
            'codigo': item_return.codigo,
            'descricao': item_return.descricao,
            'preco': item_return.preco,
            'quantidade': item_return.quantidade,
            'inativo': item_return.inativo
        }]
    }

    return make_response(jsonify(response), 200)


@item.route('/itens/consultar', methods=['GET'])
def busca_todos_itens():
    itens = item_dao.buscar_todos()

    if len(itens) == 0:
        return jsonify("Nenhum produto existente na base de dados!")

    itens_json = []
    for registro in itens:
        itens_json.append({
            'codigo': registro.codigo,
            'descricao': registro.descricao,
            'preco': registro.preco,
            'quantidade': registro.quantidade,
            'inativo': registro.inativo
        })

    response = {
        'produtos': itens_json
    }

    return make_response(jsonify(response), 200)


@item.route('/itens/atualizar/<codigo>', methods=['PUT'])
def atualiza_item(codigo):
    req = request.get_json()
    item = Item(codigo, req['descricao'], req['preco'], req['quantidade'], req['inativo'])

    item_dao.atualizar(item)

    return jsonify('Registro alterado com sucesso!')


@item.route('/itens/excluir/<codigo>', methods=['DELETE'])
def deleta_item(codigo):
    item = Item(codigo, None, None, None, None)

    item_dao.deletar(item)

    return jsonify('Item excluído com sucesso!')