from src.utils.utils import *
import psycopg2 as db
import json
import sys


class Connection:
    def __init__(self):
        with open('parameters.json', 'r') as file:
            self.dados = json.load(file)

        self.conexao = self.conexao_db()
        self.cursor = self.conexao.cursor()


    def conexao_db(self):
        parametros = {
            "host": self.dados['database'][0]['server'],
            "database": self.dados['database'][0]['dbname'],
            "user": self.dados['database'][0]['user'],
            "password": self.dados['database'][0]['password'],
            "port": self.dados['database'][0]['port']}

        try:
            conexao = db.connect(**parametros)
        except Exception as e:
            Utils.gera_log_erro("Erro ao conectar ao banco de dados! Log gerado em: ", str(e), sys._getframe().f_code.co_name)
            sys.exit(0)

        return conexao


    def query_select(self, sql):
        try:
            self.cursor.execute(sql)

            return self.cursor.fetchall()
        except Exception as e:
            Utils.gera_log_erro("Erro ao executar o comando SQL! Log gerado em: ", str(e), sys._getframe().f_code.co_name)


    def query_insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            Utils.gera_log_erro("Erro ao inserir os dados no banco de dados! ", str(e), sys._getframe().f_code.co_name)
