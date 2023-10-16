import mysql.connector

class BancoDeDados:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="KKARE7FRItLH_6cr",
            database="projeto_faculdade"
        )
        self.cursor = self.db.cursor()

    def fechar_conexao(self):
        self.db.close()
