from bancodados import BancoDeDados
import re
from kivy.app import App

class CadastroCliente(BancoDeDados):
    def insert_banco(self, values):
        self.query = """INSERT INTO projeto_faculdade.clientes
        (nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatapp_contato, fk_profissional_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        self.cursor.execute(self.query, values)
        self.db.commit()

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


    def cadastrar_cliente(self,nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp,id):

        self.validando_dados= self.existe_dados_sem_preencher(nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp)
        if self.validando_dados == False:
            self.teste, self.cpf_valido = self.validar_cpf(cpf)
            if self.teste:
                if not self.existe_cpf(self.cpf_valido):
                    if self.validar_email(email):
                        nome_completo = nome_completo.strip()
                        email = email.strip()
                        endereco = endereco.strip()
                        bairro = bairro.strip()
                        data_nascimento = data_nascimento.strip()
                        cidade = cidade.strip()
                        estado = estado.strip()
                        info = (nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, self.cpf_valido, whatsapp,id )
                        self.insert_banco(info)

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
    def recuperar_dados(self, id):
        self.query= f"""select 
                        id_cliente,
                        nome_completo, 
                        email, 
                        endereco, 
                        bairro, 
                        data_nascimento, 
                        cidade, 
                        estado, 
                        pais, 
                        cpf, 
                        whatapp_contato                
                        
                        from projeto_faculdade.clientes 
                        where fk_profissional_id = '{id}' """

        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def preencher_perfil_cliente(self, id, id_cliente):
        self.query = f"""select 
                              id_cliente,
                              nome_completo, 
                              email, 
                              endereco, 
                              bairro, 
                              data_nascimento, 
                              cidade, 
                              estado, 
                              pais, 
                              cpf, 
                              whatapp_contato                

                              from projeto_faculdade.clientes 
                              where fk_profissional_id = '{id}' and id_cliente = '{id_cliente}' """

        self.cursor.execute(self.query)
        return self.cursor.fetchall()




