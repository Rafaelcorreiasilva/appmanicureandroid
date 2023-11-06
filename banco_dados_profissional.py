from bancodados import BancoDeDados
import re


class CadastroProfissional(BancoDeDados):
   def cadastrar_profissional(self, values):
         self.query = """INSERT INTO projeto_faculdade.profissional
               (id_profissional, nome_completo, idToken, cpf, criacao_conta, data_nascimento, whatapp_contato,  email_profissional)
               VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s);
               """
         self.cursor.execute(self.query, values)
         self.db.commit()


   def validar_cpf(self,cpf):

      # Remova qualquer caractere que não seja dígito do CPF
      cpf = ''.join(filter(str.isdigit, cpf))
      cpf_valido = cpf
      # Verifique se o CPF possui 11 dígitos
      if len(cpf) != 11:
         teste= False
         return teste, cpf_valido

      # Verifique se todos os dígitos são iguais (CPF inválido)
      if cpf == cpf[0] * 11:
         teste= False
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
         return  teste , cpf_valido
      else:
         teste = False
         return teste , cpf_valido


   def conferir_celular(self,celular):
      # Remova todos os caracteres não numéricos do número
      self.numero = re.sub(r'[^0-9]', '', celular)

      # Verifique se o número possui o formato de celular brasileiro
      if re.match(r'^(55)?(0)?[1-9][0-9]{8,9}$', self.numero):
         return True
      else:
         return False

   def existe_cpf(self, cpf):
      self.query = f"SELECT cpf FROM projeto_faculdade.profissional WHERE cpf = {cpf}"

      self.cursor.execute(self.query)
      result = self.cursor.fetchone()
      return bool(result)


   def validar_dados(self,cpf):
      teste, cpf_tratado = self.validar_cpf(cpf)

      if teste:
         if not self.existe_cpf(cpf_tratado):
            mensagem = 'validado'
            return mensagem , True, cpf_tratado
         else:
            mensagem = "Este cpf ja esta em uso"
            return mensagem, False, cpf_tratado

      else:
         mensagem = 'Cpf Invalido'
         return  mensagem, False,cpf_tratado



   def existe_dados_sem_preencher(self,nome_completo,  cpf, data_nascimento, whatapp):

      if not nome_completo:
         return 'Por favor preencha todos os dados'
      elif not cpf:
         return 'Por favor preencha todos os dados'
      elif not data_nascimento:
         return 'Por favor preencha todos os dados'
      elif not whatapp:
         return 'Por favor preencha todos os dados'
      else:
         return False


   def carregar_servicos(self):
      self.query = """
      
      select 
         id_tipo_servico,
         tipo_servico, 
         tempo_estimado, 
         valor 
      from projeto_faculdade.tipo_servico"""

      self.cursor.execute(self.query)

      return self.cursor.fetchall()

   def verificar_disponibilidade_horario_agenda(self,data,horario,id_profissional):

      data = data
      horario=horario
      id_profissional= id_profissional

      self.query  = f"select * from projeto_faculdade.agenda where data = '{data}' and horario = '{horario}' and fk_profissional = '{id_profissional}'"

      self.cursor.execute(self.query)

      lista = self.cursor.fetchall()
      if len(lista) > 0:
         return 'Horario Indisponivel'

      else:
         return 'Horario livre'


   def agendar(self,values):
      dados = values
      data = dados[0]
      horario = dados[1]
      id_servico=dados[2]
      id_cliente=dados[3]
      id_profissional =dados[4]
      horario_livre = self.verificar_disponibilidade_horario_agenda(data,horario,id_profissional)
      if horario_livre == 'Horario livre':
         self.query = """
         INSERT INTO projeto_faculdade.agenda
            (data,horario,fk_id_servico,fk_id_cliente,fk_profissional)
            VALUES(%s, %s, %s,%s,%s)"""

         self.cursor.execute(self.query,values)
         self.db.commit()
         return 'agendado'
      else:
         return horario_livre

   def carregar_agenda(self,id_profissional):
      self.query = f"""           
         SELECT 
             fa.id_agenda, 
             fa.data,
             fa.horario,	
             ts.tipo_servico,	
             c.nome_completo
         FROM projeto_faculdade.agenda fa
         INNER JOIN  projeto_faculdade.tipo_servico ts
             ON fa.fk_id_servico =ts.id_tipo_servico
         INNER JOIN projeto_faculdade.clientes c
             ON c.id_cliente = fa.fk_id_cliente
         WHERE fk_profissional ='{id_profissional}' order by fa.data,fa.horario  """

      self.cursor.execute(self.query)

      return self.cursor.fetchall()

   def deletar_agendamento(self,id_profissional,data,horario,id_cliente):
      self.query = (f"""delete from projeto_faculdade.agenda where fk_profissional ={id_profissional} and data={data} and horario = {horario} and  fk_id_cliente = {id_cliente}""")

      self.cursor.execute(self.query)
      self.db.commit()