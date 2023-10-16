from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from bancodados import BancoDeDados
from banco_dados_estoque import Estoque
from banners import BannerAgenda,BannerEstoque
from banco_dados_cliente import CadastroCliente, DadosCliente
from banco_dados_profissional import CadastroProfissional
from myfirebase import Myfirebase
from functools import partial

from datetime import date, datetime, time

from kivy.clock import Clock





GUI = Builder.load_file("main.kv")
class MainApp(App):
    fornecedor = None
    produto = None
    produto_retirada = None
    id_produto_retirada = None
    id_servico = None
    id_cliente = None

    def build(self):
        self.firebase = Myfirebase()
        self.bancodados = BancoDeDados()
        self.bd_estoque = Estoque()
        self.bd_cadastro_cliente = CadastroCliente()
        self.bd_dados_clientes = DadosCliente()
        self.bd_profissional = CadastroProfissional()


        return GUI

    def on_start(self):
        try:

            self.carregar_infos_usuario()

            self.carregar_estoque()

            self.carregar_clientes_scroll()
            self.carregar_servicos()
            self.carregar_agenda()

        except:
            estoque = self.root.ids["estoquepage"]
            estoque.ids["total_estoque"].text = f'Total no estoque R$ 0.0'
        #carregar datas
        pagina_entradaretirada = self.root.ids["entradapage"]
        label_data = pagina_entradaretirada.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

        # Exibir a hora atual em um Label
        pagina_inicialpage = self.root.ids["inicialpage"]
        label_hora_atual = pagina_inicialpage.ids["id_horario_atual"]
        Clock.schedule_interval(lambda dt: self.atualizar_hora(label_hora_atual), 1)  # Atualize a cada 1 segundo
        self.atualizar_hora(label_hora_atual)  # Chame uma vez para definir a hora inicial

    def atualizar_hora(self, label):
        hora_atual = datetime.now().strftime('%H:%M')
        data_atual = date.today().strftime('%d/%m/%Y')
        label.text = f"Data: {data_atual} \n Horário: {hora_atual}"



    def carregar_servicos(self):
        agendamento_pagina = self.root.ids["agendamentopage"]
        servicos = agendamento_pagina.ids["tipo_servico"]
        servicos_lista =self.bd_profissional.carregar_servicos()

        for iten in list(servicos.children):
            servicos.remove_widget(iten)
        for servico in servicos_lista:
            id_servico = servico[0]
            info = servico[1]

            label = LabelButton(text=info,
                                 on_release=partial(self.selecionar_servico, info, id_servico))

            servicos.add_widget(label)

    def selecionar_servico(self,servico,id_servico, *args):
        self.id_servico=id_servico

        # pintar de branco todas as outras
        agendamento_pagina = self.root.ids["agendamentopage"]
        servicos = agendamento_pagina.ids["tipo_servico"]
        for item in list(servicos.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text

            if texto == servico:
                item.color = (0, 207 / 255, 219 / 255, 1)


    def carregar_clientes_scroll(self):


        lista_clientes = self.bd_dados_clientes.recuperar_dados(self.local_id)

        pagina_perfil_cliente = self.root.ids["perfilclientepage"]
        perfil_cliente = pagina_perfil_cliente.ids["escolher_cliente"]

        agendamento_pagina = self.root.ids["agendamentopage"]
        agendamento_clientes = agendamento_pagina.ids["agendamento"]


        for iten in list(perfil_cliente.children):
            perfil_cliente.remove_widget(iten)
            agendamento_clientes.remove_widget(iten)

        for cliente in lista_clientes:
            id_cliente = cliente[0]
            nome_completo = cliente[1]

            if nome_completo:
                nome_completo_fatiado = nome_completo.split()
                primeiro_nome = nome_completo_fatiado[0]
                segundo_nome = nome_completo_fatiado[1]
            else:
                nome_completo = ''


            info = f"{primeiro_nome}\n{segundo_nome}"

            label1 = LabelButton(text=info,
                                 on_release=partial(self.selecionar_cliente, info, id_cliente))

            label2 = LabelButton(text=info,
                                 on_release=partial(self.selecionar_cliente_agenda, info, id_cliente))

            perfil_cliente.add_widget(label1)
            agendamento_clientes.add_widget(label2)

    def recuperar_dados_cliente(self, id_cliente):
        cliente = self.bd_dados_clientes.preencher_perfil_cliente(self.local_id, id_cliente)
        cliente = cliente[0]

        id_cliente = cliente[0]
        nome_completo = cliente[1]
        email = cliente[2]
        endereco = cliente[3]
        bairro = cliente[4]
        data_nascimento = cliente[5]
        cidade = cliente[6]
        estado = cliente[7]
        pais = cliente[8]
        cpf = cliente[9]
        whatapp_contato = cliente[10]

        if nome_completo:
            pass
        else:
            nome_completo = ''
        nome_completo = nome_completo.capitalize()

        if email:
            pass
        else:
            email = ''
        if endereco:
            pass
        else:
         endereco = ''
        if bairro:
            pass
        else:
            bairro = ''

        if data_nascimento:
            pass
        else:
            data_nascimento = ''
        if cidade:
            pass
        else:
            cidade = ''
        if estado:
            pass
        else:
            estado = ''
        if pais:
            pass
        else:
            pais = ''
        if cpf:
            pass
        else:
            cpf = ''
        if whatapp_contato:
            pass
        else:
            whatapp_contato = ''


        perfil_cliente_pagina = self.root.ids["perfilclientepage"]
        perfil_cliente_pagina.ids["nomecliente"].text = f"Nome : {nome_completo}"
        perfil_cliente_pagina.ids["nascimentocliente"].text = f"Data de Nascimento : {data_nascimento}"
        perfil_cliente_pagina.ids["celularcliente"].text = f"Celular : {whatapp_contato}"
        perfil_cliente_pagina.ids["emailcliente"].text = f"Email : {email}"
        perfil_cliente_pagina.ids["enderecocliente"].text = f"Endereço : {endereco}"
        perfil_cliente_pagina.ids["bairrocliente"].text = f"Bairro : {bairro}"
        perfil_cliente_pagina.ids["cidadecliente"].text = f"Cidade : {cidade}"
        perfil_cliente_pagina.ids["estadocliente"].text = f"Estado: : {estado}"

    def selecionar_cliente(self, cliente, id_cliente, *args):
        self.id_cliente = id_cliente
        pagina_perfil_cliente = self.root.ids["perfilclientepage"]
        perfil_cliente = pagina_perfil_cliente.ids["escolher_cliente"]


        # pintar de branco todas as outras

        for item in list(perfil_cliente.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text

            if texto == cliente:
                item.color = (0, 207 / 255, 219 / 255, 1)
                self.recuperar_dados_cliente(id_cliente)

    def selecionar_cliente_agenda(self, cliente,id_cliente, *args):
        self.id_cliente = id_cliente
        agendamento_pagina = self.root.ids["agendamentopage"]
        perfil_cliente = agendamento_pagina.ids["agendamento"]

        # pintar de branco todas as outras

        for item in list(perfil_cliente.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text
            if texto == cliente:
                item.color = (0, 207 / 255, 219 / 255, 1)


    def carregar_estoque_retirada(self):
        lista_produtos = self.bd_estoque.recuperar_produtos()
        pagina_retirada = self.root.ids["retiradapage"]
        produtos_retirada = pagina_retirada.ids['produto_estoque']
        for iten in list(produtos_retirada.children):
            produtos_retirada.remove_widget(iten)
        for produto in lista_produtos:
            nome_produto = produto[1]
            id_produto = produto[0]
            if nome_produto:
                pass
            else:
                nome_produto = ''
            marca = produto[2]
            if marca:
                pass
            else:
                marca = ''
            cor_produto = produto[3]
            if cor_produto:
                pass
            else:
                cor_produto = ''

            produtos_lista1 = f"{nome_produto.capitalize()} \n {marca} \n {cor_produto}\n "

            label1 = LabelButton(text=produtos_lista1,
                                 on_release=partial(self.selecionar_produto_retirada, produtos_lista1, id_produto))
            produtos_retirada.add_widget(label1)



    def carregar_fornecedores_entrada(self):
        pagina_entrada = self.root.ids["entradapage"]
        fornecedores_teste = pagina_entrada.ids["fornecedor_estoque"]
        lista_fornecedores = self.bd_estoque.recuperar_fornecedor()

        for iten in list(fornecedores_teste.children):
            fornecedores_teste.remove_widget(iten)

        for fornecedor in lista_fornecedores:
            id_fornecedor = fornecedor[0]
            nome_fornecedor = fornecedor[1]
            if nome_fornecedor:
                pass
            else:
                nome_fornecedor = ''
            whatsapp = fornecedor[5]
            if whatsapp:
                pass
            else:
                whatsapp = ''
            #imagem= ImageButton()
            #lista_fornecedores.add_widget(imagem)
            dados_fornecedor = f"{nome_fornecedor.capitalize()}    \n {whatsapp}  \n   "
            label = LabelButton(text=dados_fornecedor,
                                on_release=partial(self.selecionar_fornecedor, dados_fornecedor, id_fornecedor))
            fornecedores_teste.add_widget(label)

    def carregar_produtos_entrada(self):
        pagina_entrada = self.root.ids["entradapage"]
        produtos = pagina_entrada.ids["produtos_estoque"]
        lista_produtos = self.bd_estoque.recuperar_produtos()
        for iten in list(produtos.children):
            produtos.remove_widget(iten)

        for produto in lista_produtos:
            nome_produto = produto[1]
            id_produto = produto[0]
            if nome_produto:
                pass
            else:
                nome_produto = ''
            marca = produto[2]
            if marca:
                pass
            else:
                marca = ''
            cor_produto = produto[3]
            if cor_produto:
                pass
            else:
                cor_produto = ''

            produtos_lista = f"{nome_produto.capitalize()} \n {marca} \n {cor_produto}\n "

            label = LabelButton(text=produtos_lista,
                                on_release=partial(self.selecionar_produto, produtos_lista, id_produto))
            produtos.add_widget(label)

    def carregar_infos_usuario(self):
        try:
            with open("refrestoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)

            self.local_id = local_id
            self.id_token = id_token
            self.mudar_tela("inicialpage")
            self.carregar_estoque()

        except Exception as e:
            print(e)
    def carregar_agenda(self):

        agenda = self.root.ids["agendapage"].ids["agenda_lista"]
        for iten in list(agenda.children):
            agenda.remove_widget(iten)
        agenda_bd = self.bd_profissional
        agenda_horario = agenda_bd.carregar_agenda(self.local_id)
        for iten in agenda_horario:
            id_agenda=iten[0]
            nome_completo = iten[4]
            data = iten[1]
            horario = iten[2]
            tipo_servico = iten[3]
            info = f'{nome_completo} -- {horario} -- {data} -- {tipo_servico}'
            print(info)
            label = LabelButton(text=info,
                                on_release=partial(self.selecionar_cliente_agenda_cancelar, info, id_agenda))
            agenda.add_widget(label)

    def selecionar_cliente_agenda_cancelar(self, cliente, id_agenda, *args):
        self.id_agenda = id_agenda
        agenda = self.root.ids["agendapage"].ids["agenda_lista"]

        # pintar de branco todas as outras

        for item in list(agenda.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text

            if texto == cliente:
                item.color = (0, 207 / 255, 219 / 255, 1)

    def carregar_estoque(self):
        estoque = self.root.ids["estoquepage"].ids["estoque_lista"]
        for iten in list(estoque.children):
            estoque.remove_widget(iten)

        queries_banco_dados_estoque = self.bd_estoque
        estoque_itens = queries_banco_dados_estoque.recuperar_dados_estoque(self.local_id)

        for itens in estoque_itens:
            nome_produto = itens[0]
            quantidade_estoque = itens[1]
            quantidade_saida = itens[2]
            quantidade_total = int(quantidade_estoque) - int(quantidade_saida)
            if quantidade_total > 0:
                banner_estoque = BannerEstoque(quantidade=quantidade_total, fk_id_produto_estoque=nome_produto)
                estoque.add_widget(banner_estoque)
            else:
                pass

        total_estoque = self.bd_estoque.total_estoque(self.local_id)
        if not total_estoque:
            total_estoque = 0.0
        else:
            pass
        pagina_entradaretirada = self.root.ids["estoquepage"]
        pagina_entradaretirada.ids["total_estoque"].text = f'Total no estoque R$ {total_estoque}'
        self.carregar_produtos_entrada()
        self.carregar_fornecedores_entrada()
        self.carregar_estoque_retirada()

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def selecionar_fornecedor(self, fornecedor,id_fornecedor, *args):
        self.fornecedor = fornecedor
        self.id_fornecedor = id_fornecedor
        # pintar de branco todas as outras
        pagina_entradaretirada = self.root.ids["entradapage"]
        fornecedores = pagina_entradaretirada.ids["fornecedor_estoque"]

        for item in list(fornecedores.children):
            item.color = (1, 1, 1, 1)
        # pintar de azul o item que selecionamos
            texto = item.text
            if texto == fornecedor:
                item.color = (0, 207/255, 219/255, 1)

    def selecionar_produto(self, produto, id_produto, *args):
        self.produto= produto
        self.id_produto = id_produto
        # pintar de branco todas as outras
        pagina_entradaretirada = self.root.ids["entradapage"]
        produtos = pagina_entradaretirada.ids["produtos_estoque"]

        for item in list(produtos.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text
            if texto == produto:
                item.color = (0, 207 / 255, 219 / 255, 1)

    def selecionar_produto_retirada(self, produto, id_produto, *args):

        self.produto_retirada = produto
        self.id_produto_retirada = id_produto
        # pintar de branco todas as outras
        pagina_entradaretirada = self.root.ids["retiradapage"]
        produtos = pagina_entradaretirada.ids["produto_estoque"]

        for item in list(produtos.children):
            item.color = (1, 1, 1, 1)
            # pintar de azul o item que selecionamos
            texto = item.text
            if texto == produto:
                item.color = (0, 207 / 255, 219 / 255, 1)

    def retirada_produto(self):

        produto = self.produto_retirada
        id_produto = self.id_produto_retirada
        pagina_retirada = self.root.ids["retiradapage"]
        quantidade = pagina_retirada.ids["quantidade"].text

        if not quantidade:
            pagina_retirada.ids["text_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = int(quantidade)
            except:
                pagina_retirada.ids["text_quantidade"].color = (1, 0, 0, 1)
        if not produto:
            pagina_retirada.ids["selecione_produto"].color = (1, 0, 0, 1)

        # dado que ele preencheu tudo vamos popular a tabela
        if produto and quantidade and type(quantidade) == int and id_produto:
            id_profissional = self.local_id

            mensagem = self.bd_estoque.retirar_produto(id_produto= id_produto, id_profissional=id_profissional, quantidade_para_retirada=quantidade)
            if mensagem == "produto retirado com sucesso":
                self.carregar_estoque()
                retirada= self.root.ids['retiradapage']
                retirada_produto = retirada.ids['mensagem_add']
                retirada_produto.text = mensagem
                retirada_produto.color = (0, 207 / 255, 219 / 255, 1)

            else:
                retirada = self.root.ids['retiradapage']
                retirada_produto = retirada.ids['mensagem_add']
                retirada_produto.text = mensagem
                retirada_produto.color = (1, 0, 0, 1)
        else:
            retirada = self.root.ids['retiradapage']
            retirada_produto = retirada.ids['mensagem_add']
            retirada_produto.text = 'Preencha corretamente todas informações'
            retirada_produto.color = (1, 0, 0, 1)
        #pintar tudo de branco denovo
        pagina_entradaretirada = self.root.ids["retiradapage"]
        produtos = pagina_entradaretirada.ids["produto_estoque"]
        pagina_retirada.ids["quantidade"].text = ''
        for item in list(produtos.children):
            item.color = (1, 1, 1, 1)

        self.produto_retirada = None
        self.id_produto_retirada = None

    def agendar_cliente(self):
        pagina_agenda = self.root.ids["agendamentopage"]
        id_cliente = self.id_cliente
        dia = pagina_agenda.ids["dia"].text
        mes = pagina_agenda.ids["mes"].text
        ano = pagina_agenda.ids["ano"].text
        hora = pagina_agenda.ids["hora"].text
        minuto = pagina_agenda.ids["minuto"].text
        servico = self.id_servico

        if not id_cliente:
            pagina_agenda.ids["selecione_cliente"].color = (1, 0, 0, 1)
        if dia:
            try:
                dia = int(dia)
                if dia > 31:
                    pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)


            except:
                pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)
        else:
            pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)


        if mes:
            try:
                mes = int(mes)
                if mes > 12:
                    pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)
            except:
                pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)
        else:
            pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)


        if ano:
            try:
                 ano = int(ano)
                 if ano < int(datetime.now().year):
                    pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)
            except:
                    pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)
        else:
            pagina_agenda.ids["escolher_dia_agendamento"].color = (1, 0, 0, 1)


        if hora:
            try:
                hora = int(hora)
                if hora > 23:
                    pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)
            except:
                pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)
        else:
            pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)


        if minuto:
                try:
                    minuto = int(minuto)
                    if minuto > 59:
                        pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)
                except:
                    pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)
        else:
            pagina_agenda.ids["horario_agendamento"].color = (1, 0, 0, 1)

        if not servico:
            pagina_agenda.ids["agendamento_servico"].color = (1, 0, 0, 1)


        if servico and minuto \
                and type(minuto) == int and hora \
                and type(hora) == int \
                and type(mes) == int and mes and ano \
                and type(ano) == int and dia \
                and type(dia) == int and id_cliente\
                and minuto < 60 and hora < 23 and ano >= int(datetime.now().year) \
                and mes < 13 and dia < 32:

            id_cliente = self.id_cliente
            id_servico = self.id_servico
            id_profissional = self.local_id
            horario = time(hora, minuto)
            data = date(ano, mes, dia)

            info = (data,horario,id_servico,id_cliente,id_profissional)
            self.bd_profissional.agendar(info)
            pagina_agenda = self.root.ids["agendamentopage"]
            agedamento = pagina_agenda.ids['agendamento']
            tipo_servico = pagina_agenda.ids['tipo_servico']
            for item in list(agedamento.children):
                item.color = (1, 1, 1, 1)
            for item in list(tipo_servico.children):
                item.color = (1, 1, 1, 1)
            pagina_agenda = self.root.ids['agendamentopage']
            mensagem = pagina_agenda.ids['mensagem_add']
            mensagem.text = f'Agendado com sucesso'
            mensagem.color = (0, 207/255, 219/255, 1)

        else:
            pagina_agenda = self.root.ids['agendamentopage']
            mensagem = pagina_agenda.ids['mensagem_add']
            mensagem.text = f'Erro ao tentar agendar tente novamente'
            mensagem.color = (1, 0, 0, 1)
            # pintar tudo de branco denovo
            pagina_agenda = self.root.ids["agendamentopage"]
            agedamento = pagina_agenda.ids['agendamento']
            tipo_servico = pagina_agenda.ids['tipo_servico']
            pagina_agenda.ids["dia"].text = ''
            pagina_agenda.ids["mes"].text = ''
            pagina_agenda.ids["ano"].text = ''
            pagina_agenda.ids["hora"].text= ''
            pagina_agenda.ids["minuto"].text = ''
            for item in list(agedamento.children):
                item.color = (1, 1, 1, 1)
            for item in list(tipo_servico.children):
                item.color = (1, 1, 1, 1)

        self.id_cliente = None
        self.id_servico = None



    def entrada_produto(self):

        fornecedor = self.fornecedor
        produto = self.produto
        pagina_entrada = self.root.ids["entradapage"]
        data = pagina_entrada.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_entrada.ids["preco_unitario"].text
        quantidade = pagina_entrada.ids["quantidade"].text
        if not fornecedor:
            pagina_entrada.ids["selecione_fornecedor"].color = (1, 0, 0, 1)
        if not produto:
            pagina_entrada.ids["selecione_produto"].color = (1, 0, 0, 1)
        if not preco:
            pagina_entrada.ids["text_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_entrada.ids["text_preco"].color = (1, 0, 0, 1)

        if not quantidade:
            pagina_entrada.ids["text_quantidade"].color = (1, 0, 0, 1)

        else:
            try:
                quantidade = int(quantidade)
            except:
                pagina_entrada.ids["text_quantidade"].color = (1, 0, 0, 1)


        #dado que ele preencheu tudo vamos popular a tabela
        if fornecedor and produto and preco and quantidade and type(preco) == float and type(quantidade) == int:
            id_fornecedor = self.id_fornecedor
            id_produto = self.id_produto
            id_profissional = self.local_id
            info = (quantidade, preco, id_fornecedor, id_produto, id_profissional)
            self.bd_estoque.entrada_produtos(info)
            entrada = self.root.ids['entradapage']
            produto_add = produto.split('\n')[0]
            entrada_produto = entrada.ids['mensagem_add']
            entrada_produto.text = f'{produto_add} adicionado com sucesso'
            entrada_produto.color = (0, 207/255, 219/255, 1)

            # atualizar banco de dados
            self.carregar_estoque()

            pagina_entradaretirada = self.root.ids["entradapage"]
            produtos = pagina_entradaretirada.ids["produtos_estoque"]
            fornecedor = pagina_entradaretirada.ids["fornecedor_estoque"]
            for item in list(produtos.children):
                item.color = (1, 1, 1, 1)
            for item in list(fornecedor.children):
                item.color = (1, 1, 1, 1)
            pagina_entradaretirada.ids["preco_unitario"].text = ''
            pagina_entradaretirada.ids["quantidade"].text = ''

        else:
            entrada = self.root.ids['entradapage']
            entrada_produto = entrada.ids['mensagem_add']
            entrada_produto.text = f'Erro ao tentar cadastrar tente novamente'
            entrada_produto.color = (1, 0, 0, 1)
            # pintar tudo de branco denovo
            pagina_entradaretirada = self.root.ids["entradapage"]
            produtos = pagina_entradaretirada.ids["produtos_estoque"]
            fornecedor = pagina_entradaretirada.ids["fornecedor_estoque"]
            for item in list(produtos.children):
                item.color = (1, 1, 1, 1)
            for item in list(fornecedor.children):
                item.color = (1, 1, 1, 1)
            pagina_entradaretirada.ids["preco_unitario"].text = ''
            pagina_entradaretirada.ids["quantidade"].text = ''

        self.fornecedor = None
        self.produto = None


    def cadastrar_cliente(self, nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp):
        self.bd_cadastro_cliente.cadastrar_cliente(nome_completo, email, endereco, bairro, data_nascimento, cidade, estado, cpf, whatsapp, self.local_id)

MainApp().run()
