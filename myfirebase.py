import requests
from kivy.app import App
from banco_dados_cadastro_profissional import CadastroProfissional
class Myfirebase():
    API_KEY="AIzaSyD9RKSbnABUsYOMM4dyzEBWt9bPL3eyusU"

    def criar_conta(self, email, senha, nome_completo,  cpf, data_nascimento, whatapp):

        self.bancodados =CadastroProfissional()
        validando_dados = self.bancodados.existe_dados_sem_preencher(nome_completo,  cpf, data_nascimento, whatapp)
        if validando_dados == False:
            link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'

            info = {'email': email,
                    'password': senha,
                    'returnSecureToken': True}
            mensagem , valida_cpf,cpf_tratado = self.bancodados.validar_dados(cpf)

            if valida_cpf:
                print('cpf valido')
                requisicao = requests.post(link, data=info)
                requisicao_dic = requisicao.json()


                if requisicao.ok:


                    id_token = requisicao_dic["idToken"] # autenticação
                    refresh_token = requisicao_dic["refreshToken"] # mantem o usuario logado
                    local_id = requisicao_dic["localId"] # id_usuario

                    meu_aplicativo = App.get_running_app()
                    meu_aplicativo.local_id= local_id
                    meu_aplicativo.id_token = id_token

                    with open("refrestoken.txt", "w") as arquivo:
                        arquivo.write(refresh_token)
                    print('vaicadastrar')
                    #salavar as informção noi banco de dados {local_id} é o id do ususario
                    self.cadastrar_profissional = CadastroProfissional()
                    info_usuario = (local_id, nome_completo, id_token, cpf_tratado, data_nascimento, whatapp, email)
                    print(info_usuario)
                    self.cadastrar_profissional.cadastrar_profissional(info_usuario)
                    meu_aplicativo.carregar_infos_usuario()
                    meu_aplicativo.mudar_tela("inicialpage")



                else:
                    mensagem_erro = requisicao_dic['error']['message']
                    meu_aplicativo = App.get_running_app()
                    pagina_login = meu_aplicativo.root.ids["cadastropage"]
                    pagina_login.ids["mensagem_cadastro"].text = mensagem_erro
                    pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)
                print(requisicao_dic)
            else:
                meu_aplicativo = App.get_running_app()
                pagina_login = meu_aplicativo.root.ids["cadastropage"]
                pagina_login.ids["mensagem_cadastro"].text = mensagem
                pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)
        else:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["cadastropage"]
            pagina_login.ids["mensagem_cadastro"].text = validando_dados
            pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)


    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {'email': email,
                'password': senha,
                'returnSecureToken': True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            id_token = requisicao_dic["idToken"]  # autenticação
            refresh_token = requisicao_dic["refreshToken"]  # mantem o usuario logado
            local_id = requisicao_dic["localId"]  # id_usuario

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refrestoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)


            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("inicialpage")



        else:
            mensagem_erro = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)



    def trocar_token(self,refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        requisicao = requests.post(link,data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic['user_id']
        id_token = requisicao_dic['id_token']
        return local_id, id_token

