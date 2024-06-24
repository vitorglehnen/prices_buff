from flask import jsonify, request, Blueprint, make_response
from src.connection.connect import Connection


conexao = Connection().cursor()
cursor_sql = conexao.cursor()
item = Blueprint('item', __name__)


@item.route('/itens/incluir', methods=['POST'])
def itens_incluir():
    codigo = request.json['codbuff']
    nome = request.json['nome']
    preco = request.json['preco']
    quantidade = request.json['quantidade']

    if codigo == '':
        response = {"response": "O valor de codbuff não pode estar vazio!"}

        return jsonify(response['response'])

    cursor_sql.execute(f"""
                    INSERT INTO public.item(coditem, descricao, preco, quantidade, inativo)
	                VALUES ({codigo},'{nome}', {preco}, {quantidade}, 'N')
                    """)

    conexao.commit()
    cursor_sql.close()

    return jsonify('Item inserido com sucesso!')


@item.route('/itens/consultarCodigo/<codigo>', methods=['GET'])
def busca_item(codigo):
    cursor_sql.execute(f"""
                    SELECT i.coditem, i.descricao, i.preco, i.quantidade, i.inativo
                    FROM public.item i
                    WHERE i.coditem = {codigo}
                    """)

    dataset = cursor_sql.fetchall()
    cursor_sql.close()

    if len(dataset) == 0:
        return jsonify("Código de produto inexistente na base de dados!")

    response = {
        'codigo': dataset[0][0],
        'descricao': dataset[0][1],
        'preco': dataset[0][2],
        'quantidade': dataset[0][3],
        'inativo': dataset[0][4]
    }

    return jsonify(response)


@item.route('/itens/consultar', methods=['GET'])
def busca_todos_itens():
    cursor = conexao.cursor()

    cursor.execute(f"""
                    SELECT i.coditem, i.descricao, i.preco, i.quantidade, i.inativo
                    FROM item i
                    """)

    dataset = cursor.fetchall()
    cursor.close()

    if len(dataset) == 0:
        return jsonify("Nenhum produto existente na base de dados!")

    produtos = []

    for registro in dataset:
        produtos.append({
            'codigo': registro[0],
            'descricao': registro[1],
            'preco': registro[2],
            'quantidade': registro[3],
            'inativo': registro[4]
        })
        
    response = {
        'produtos': produtos
    }

    return make_response(jsonify(response), 200)


@item.route('/itens/alterar/<codigo>', methods=['PUT'])
def altera_item(codigo):
    dados = request.get_json()

    cursor_sql.execute(f"""
                    UPDATE item SET
                    descricao = '{dados['descricao']}',
                    quantidade = {dados['quantidade']},
                    preco = {dados['preco']},
                    inativo = '{dados['inativo']}'
                    WHERE coditem = {codigo}                  
                   """)

    conexao.commit()

    return jsonify('Registro alterado com sucesso!')


@item.route('/itens/excluir/<codigo>', methods=['DELETE'])
def deleta_item(codigo):
    cursor_sql.execute(f"""
                    DELETE FROM item
                    WHERE coditem = {codigo}                 
                   """)

    conexao.commit()

    return jsonify('Item excluído com sucesso!')
