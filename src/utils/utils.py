import datetime
import json
import sys
import os


class Utils:
    @staticmethod
    def retorna_parameters_json():
        if not os.path.exists('parameters.json'):
            dados = {
                "database": [
                    {
                        "user": "",
                        "password": "",
                        "dbname": "",
                        "server": "",
                        "port": ""
                    }
                ],
                "email": [
                    {
                        "endereco_remetente": "",
                        "endereco_destinatario": "",
                        "senha": ""
                    }
                ]
            }

            with open('parameters.json', 'w') as file:
                json.dump(dados, file, indent=2)

        with open('parameters.json', 'r') as file:
            parameters = json.load(file)

        return parameters


    @staticmethod
    def gera_log_erro(titulo, erro, funcao):
        nome_arquivo = f'log-{datetime.datetime.now().date()}.txt'
        caminho_exe = os.path.dirname(os.path.abspath(__file__))

        with open(nome_arquivo, 'a') as file:
            file.write(f'Data:{datetime.datetime.now().date()} Hora:{datetime.datetime.now().time().strftime("%H:%M:%S")}')
            file.write('\n')
            file.write('Erro na função:' + funcao)
            file.write('\n\n')
            file.write(erro)
            file.write('\n')
            file.write('----------------------------------------------------------------------------------------')
            file.write('\n')

        print(titulo + ' Log gerado em: ' + caminho_exe + '\\' + nome_arquivo)

        exit()


    @staticmethod
    def get_diretorio_exe():
        if getattr(sys, 'frozen', False):
            # Quando o código está sendo executado a partir de um executável (EXE)
            return os.path.dirname(sys.executable)
        else:
            # Quando o código é executado como um script Python
            return os.path.dirname(os.path.abspath(__file__))