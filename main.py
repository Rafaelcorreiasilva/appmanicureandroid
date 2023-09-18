from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from bancodados import BancoDeDados
from banco_dados_estoque import Estoque
from banners import BannerAgenda,BannerEstoque
from banco_dados_cliente import CadastroCliente, DadosCliente
from myfirebase import Myfirebase
from functools import partial
from datetime import date, datetime
from kivy.clock import Clock



GUI = Builder.load_file("main.kv")
class MainApp(App):
    fornecedor = None
    produto = None
    produto_retirada = None
    id_produto_retirada = None

    def build(self):
        self.firebase = Myfirebase()
        self.bancodados = BancoDeDados()
        self.cadastracliente = CadastroCliente()
        self.cliente = DadosCliente()
        self.bd_estoque = Estoque()

        return GUI

    def on_start(self):
        self.carregar_infos_usuario()
        self.carregar_estoque()

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
            banner_estoque = BannerEstoque(quantidade=quantidade_total, fk_id_produto_estoque=nome_produto)
            estoque.add_widget(banner_estoque)
        total_estoque = self.bd_estoque.total_estoque(self.local_id)
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

MainApp().run()
