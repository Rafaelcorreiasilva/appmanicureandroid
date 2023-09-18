from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class BannerAgenda(GridLayout):

    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        cliente = kwargs["cliente"]
        horario = kwargs["horario"]
        data = kwargs["data"]
        servico = kwargs["servico"]

        esquerda = FloatLayout()
        esquerda_texto = Label( text=f"{cliente}", size_hint=(1, 0.6), pos_hint={"right": 1, "top": 0.6})
        esquerda.add_widget(esquerda_texto)

        meio = FloatLayout()
        meio_texto = Label(text=f"{horario}  -   {data}", size_hint=(1, 0.6), pos_hint={"right": 1, "top": 0.6})
        meio.add_widget(meio_texto)

        direita = FloatLayout()
        direita_texto = Label(text=f"{servico}", size_hint=(1, 0.6), pos_hint={"right": 1, "top": 0.6})
        direita.add_widget(direita_texto)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size



class BannerEstoque(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        quantidade = int(kwargs['quantidade'])
        #preco = kwargs['valor_unitario']
        produto = kwargs['fk_id_produto_estoque']


        esquerda = FloatLayout()
        esquerda_texto = Label(text=f"produto: {produto}", size_hint=(1, 0.33), pos_hint={"right": 1, "top": 0.95})
        #esquerda_texto2 = Label(text=f"fornecedor: {fornecedor}", size_hint=(1, 0.4), pos_hint={"right": 1, "top": 0.4})
        esquerda.add_widget(esquerda_texto)
        #esquerda.add_widget(esquerda_texto2)

        meio = FloatLayout()
        meio_texto = Label(text=f"quantidade: {quantidade}", size_hint=(1, 0.33), pos_hint={"right": 1, "top": 0.95})
        #meio_texto2 = Label(text=f"valor unitário R$ {preco}", size_hint=(1, 0.4), pos_hint={"right": 1, "top": 0.4})
        meio.add_widget(meio_texto)
        #meio.add_widget(meio_texto2)

        #direita = FloatLayout()
       # direita_texto = Label(text=f"entrada: {entrada}", size_hint=(1, 0.33), pos_hint={"right": 1, "top": 0.95})
        #direita_texto2 = Label(text=f"saida: {saida}", size_hint=(1, 0.4), pos_hint={"right": 1, "top": 0.4})
        #direita.add_widget(direita_texto)
        #direita.add_widget(direita_texto2)
        self.add_widget(esquerda)
        self.add_widget(meio)
        #self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size
