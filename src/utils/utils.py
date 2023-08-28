import json
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
