import mysql.connector

class BancoDeDados:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        self.cursor = self.db.cursor()

    def fechar_conexao(self):
        self.db.close()
