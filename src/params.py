import configparser
import psycopg2 as db
import sys
import os


caminho_exe = os.path.abspath(sys.argv[0])
caminho_parameters_ini = os.path.dirname(caminho_exe) + r"\parameters.ini"


def cria_parameters_ini():
    ini = configparser.ConfigParser()
    ini.read(caminho_parameters_ini)

    return ini


def conexao_db():
    ini = cria_parameters_ini()

    parametros = {
        "host": ini.get('DATABASE', 'Server'),
        "database": ini.get('DATABASE', 'DatabaseName'),
        "user": ini.get('DATABASE', 'User'),
        "password": ini.get('DATABASE', 'Password')}

    conexao = db.connect(**parametros)

    return conexao


conexao_db()