from bancodados import BancoDeDados


class Estoque(BancoDeDados):
    def recuperar_fornecedor(self):
         self.query = """
         SELECT
            id_fornecedor,
            nome,
            cnpj,
            endereco,
            email,
            whatapp_contato 
         FROM projeto_faculdade.fornecedor
               """
         self.cursor.execute(self.query)

         return self.cursor.fetchall()

    def entrada_produtos(self, values):
        self.query = f"""INSERT INTO projeto_faculdade.estoque
                       (quantidade, valor_unitario, fk_id_fornecedor, fk_id_produto_estoque,fk_profissional_id)
                       VALUES(%s, %s, %s, %s, %s);"""

        self.cursor.execute(self.query, values)
        self.db.commit()
    def recuperar_produtos(self):
        self.query = """
             SELECT
                id_produto,
                nome_produto,
                marca_produto,
                tipo_produto,
                cor_produto,
                colecao  
            FROM projeto_faculdade.produtos
                    """
        self.cursor.execute(self.query)

        return self.cursor.fetchall()

    def total_estoque(self, id):
        self.query = f"""select 
                      FORMAT(sum((e.valor_unitario * e.quantidade)) - sum(e.quantidade_saida),2) as total_estoque
                      FROM projeto_faculdade.estoque e	
                      WHERE e.fk_profissional_id  = '{id}'"""
        self.cursor.execute(self.query)
        resultado = self.cursor.fetchone()
        return resultado[0]

    def recuperar_dados_estoque(self, id):

        query = f"""
                select 
                p.nome_produto,
                round(sum(e.quantidade),2) as quantidade_estoque,
                round(sum(e.quantidade_saida),2) as quantidade_saida 
                FROM projeto_faculdade.estoque e
                    INNER JOIN projeto_faculdade.produtos p
                        ON e.fk_id_produto_estoque = p.id_produto
                WHERE e.fk_profissional_id  = '{id}'
                GROUP BY fk_id_produto_estoque                
                """
        try:
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()

            return resultado

        except:
           print("Não achou")

    def retirar_produto(self, id_produto, id_profissional, quantidade_para_retirada):
            registro_antigo = self.registro_antigo_produto(id=id_produto, id_profissional=id_profissional)
            if registro_antigo == None:
                return 'Este produto não tem disponivel no estoque'
            else:
                valor_estoque = self.verificacao_possibilidade_retirada(id_profissional=id_profissional,id_produto=id_produto)
                verificacao_possibilidade_retirada = valor_estoque - quantidade_para_retirada
                if verificacao_possibilidade_retirada < 0:
                    return 'Ação negada..Esta tentando retirar quantidade maior que o disponivel em estoque'
                else:

                    while True:
                        id_registro, data, quantidade, quantidade_saida = self.registro_antigo_produto(id=id_produto, id_profissional=id_profissional)
                        quantidade_produto_disponivel = quantidade - quantidade_saida

                        if quantidade_produto_disponivel >= quantidade_para_retirada:
                            valor_para_retirar = quantidade_para_retirada + quantidade_saida


                            self.update_estoque(valor_para_retirar, id_registro, id_profissional)
                            break
                        elif quantidade_para_retirada > quantidade_produto_disponivel:
                            valor_para_retirar = quantidade_saida + quantidade_produto_disponivel
                            self.update_estoque(valor_para_retirar, id_registro, id_profissional)
                            quantidade_para_retirada -= quantidade_produto_disponivel
                    return 'produto retirado com sucesso'

    def update_estoque(self, valor_atualizado, id_registro, id_profissional):
        self.query = f"""UPDATE projeto_faculdade.estoque
                         SET quantidade_saida = {valor_atualizado},
                         data_saida=CURRENT_TIMESTAMP
                         where id_cadastro = {id_registro} and fk_profissional_id = '{id_profissional}'"""

        self.cursor.execute(self.query)
        self.db.commit()
    def verificacao_possibilidade_retirada(self, id_produto, id_profissional):
        self.query = f"""
                        SELECT sum(quantidade)-sum(quantidade_saida) as quantidade_disponivel
                        FROM projeto_faculdade.estoque
                        WHERE fk_profissional_id = '{id_profissional}' and fk_id_produto_estoque = {id_produto}
                """
        self.cursor.execute(self.query)
        result = self.cursor.fetchone()

        return result[0]
    def registro_antigo_produto(self, id, id_profissional):
        self.query = f"""SELECT 
                            id_cadastro, 
                            data_entrada,
                            quantidade,
                            quantidade_saida 
                        FROM projeto_faculdade.estoque 
                        WHERE fk_id_produto_estoque = {id} AND
                         (quantidade - quantidade_saida) > 0 and fk_profissional_id = '{id_profissional}' ORDER BY data_entrada asc limit 1"""

        self.cursor.execute(self.query)
        result = self.cursor.fetchone()

        return result

