from bancodados import BancoDeDados
import re
from kivy.app import App

class CadastroCliente(BancoDeDados):
    def insert_banco(self, values):
        self.query = """INSERT INTO projeto_faculdade.clientes
        (nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, pais, cpf, criacao_conta, whatapp_contato, foto_cliente, fk_profissional_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, 'Brasil', %s, CURRENT_TIMESTAMP, %s, '0', %s);
        """

        self.cursor.execute(self.query, values)
        self.db.commit()
        self.fechar_conexao()
        print('cadastrado')



    def validar_cpf(self, cpf):

        # Remova qualquer caractere que não seja dígito do CPF
        cpf = ''.join(filter(str.isdigit, cpf))
        cpf_valido = cpf
        # Verifique se o CPF possui 11 dígitos
        if len(cpf) != 11:
            teste = False
            return teste, cpf_valido

        # Verifique se todos os dígitos são iguais (CPF inválido)
        if cpf == cpf[0] * 11:
            teste = False
            return teste, cpf_valido
        # Calcule o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = 11 - (soma % 11)
        if resto in (10, 11):
            digito_verificador1 = 0
        else:
            digito_verificador1 = resto

        # Calcule o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = 11 - (soma % 11)
        if resto in (10, 11):
            digito_verificador2 = 0
        else:
            digito_verificador2 = resto

        # Verifique se os dígitos verificadores estão corretos
        if int(cpf[9]) == digito_verificador1 and int(cpf[10]) == digito_verificador2:
            teste = True
            return teste, cpf_valido
        else:
            teste = False
            return teste, cpf_valido

    def existe_cpf(self, cpf):
        self.query = f"SELECT cpf FROM projeto_faculdade.clientes WHERE cpf = {cpf}"

        self.cursor.execute(self.query)
        result = self.cursor.fetchone()
        return bool(result)

    def existe_dados_sem_preencher(self,nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp):

        if not nome_completo:
            return 'Por favor preencha todos os dados'
        elif not email:
            return 'Por favor preencha todos os dados'
        elif not data_nascimento:
            return 'Por favor preencha todos os dados'
        elif not endereco:
            return 'Por favor preencha todos os dados'
        elif not bairro:
            return 'Por favor preencha todos os dados'
        elif not cidade:
            return 'Por favor preencha todos os dados'
        elif not estado:
            return 'Por favor preencha todos os dados'
        elif not cpf:
            return 'Por favor preencha todos os dados'
        elif not data_nascimento:
            return 'Por favor preencha todos os dados'
        elif not whatsapp:
            return 'Por favor preencha todos os dados'
        else:
            return False

    def validar_email(self,email):
        # Padrão de expressão regular para validação básica de e-mail
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Verifique se o e-mail corresponde ao padrão
        if re.match(padrao, email):
            return True
        else:
            return False

    def cadastrar_cliente(self,nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp,id_profissional):
        self.validando_dados= self.existe_dados_sem_preencher(nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp)
        if self.validando_dados == False:
            self.teste, self.cpf_valido = self.validar_cpf(cpf)
            if self.teste:
                if not self.existe_cpf(self.cpf_valido):
                    if self.validar_email(email):
                        self.insert_banco((nome_completo, email, endereco, bairro, data_nascimento, cidade, estado,self.cpf_valido, whatsapp,id_profissional))
                        meu_aplicativo = App.get_running_app()
                        meu_aplicativo.mudar_tela("perfilclientepage")
                    else:
                        meu_aplicativo = App.get_running_app()
                        pagina_login = meu_aplicativo.root.ids["cadastroclientepage"]
                        pagina_login.ids["mensagem_cadastro"].text = 'email inválido'
                        pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)

                else:
                    meu_aplicativo = App.get_running_app()
                    pagina_login = meu_aplicativo.root.ids["cadastroclientepage"]
                    pagina_login.ids["mensagem_cadastro"].text = 'cliente ja cadastrado'
                    pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)
            else:
                meu_aplicativo = App.get_running_app()
                pagina_login = meu_aplicativo.root.ids["cadastroclientepage"]
                pagina_login.ids["mensagem_cadastro"].text = 'cpf inválido'
                pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)

        else:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["cadastroclientepage"]
            pagina_login.ids["mensagem_cadastro"].text = self.validando_dados
            pagina_login.ids["mensagem_cadastro"].color = (1, 0, 0, 1)

class DadosCliente(BancoDeDados):
    def recuperar_dados(self):
        self.query= """select nome_completo, 
                        email, 
                        endereco, 
                        bairro, 
                        data_nascimento, 
                        cidade, 
                        estado, 
                        pais, 
                        cpf, 
                        whatapp_contato, 
                        foto_cliente, 
                        fk_profissional_id 
                        from projeto_faculdade.clientes 
                        where fk_profissional_id = 'NoMnYY9OrGRToY8sZqjxOwH6IIz1' 
                        """

        self.cursor.execute(self.query)
        result = self.cursor.fetchone()
        nome_completo = result[0]
        email = result[1]
        endereco = result[2]
        bairro = result[3]
        data_nascimento = result[4]
        cidade = result[5]
        estado = result[6]
        pais = result[7]
        cpf = result[8]
        whatapp_contato = result[9]
        foto_cliente = result[10]
        fk_profissional_id = result[11]
        return nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, pais, cpf, whatapp_contato, foto_cliente, fk_profissional_id



