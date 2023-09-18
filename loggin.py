import requests
import certifi
import os

os.environ["SSL_CERT_FILE"] = certifi.where()
class Login():
    API_KEY = ""

    def criar_conta(self, email, senha):
        link = "https://"

        info = {"email": email,
                "senha": senha,
                "returnSecureToken": True}
        requisicao = requests.pos(link, data=info)

    def fazer_login(self, email, senha):
        pass