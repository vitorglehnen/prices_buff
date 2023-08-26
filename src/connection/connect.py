from exceptions.connectiondb import ConnectionDatabaseException
import configparser
import psycopg2 as db
import sys
import os


class Connection:
    def __init__(self):
        caminho_exe = os.path.abspath(sys.argv[0])
        self.caminho_parameters_ini = os.path.dirname(caminho_exe) + r"\parameters.ini"

    def cria_parameters_ini(self):
        ini = configparser.ConfigParser()
        ini.read(self.caminho_parameters_ini)

        return ini

    def conexao_db(self):
        ini = self.cria_parameters_ini()

        parametros = {
            "host": ini.get('DATABASE', 'Server'),
            "database": ini.get('DATABASE', 'DatabaseName'),
            "user": ini.get('DATABASE', 'User'),
            "password": ini.get('DATABASE', 'Password')}

        conexao = db.connect(**parametros)

        return conexao




