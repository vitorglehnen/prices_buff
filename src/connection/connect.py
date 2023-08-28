import psycopg2 as db
import json
import os


class Connection:
    def __init__(self):
        with open('parameters.json', 'r') as file:
            self.dados = json.load(file)

    def conexao_db(self):
        parametros = {
            "host": self.dados['database'][0]['server'],
            "database": self.dados['database'][0]['dbname'],
            "user": self.dados['database'][0]['user'],
            "password": self.dados['database'][0]['password'],
            "port": self.dados['database'][0]['port']}

        conexao = db.connect(**parametros)

        return conexao
