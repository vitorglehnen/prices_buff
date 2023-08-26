from src.connection.connect import Connection


class Item:
    def __init__(self):
        conexao_instance = Connection

        self.conexao = conexao_instance.conexao_db()
        self.query = self.conexao.cursor()

    def get_codigo_itens(self):
        sql = """
        SELECT coditem FROM item
        """

        self.query.execute('SELECT coditem FROM item')
        result = self.query.fetchall()

        self.query.close()
        self.conexao.close()

        return result
