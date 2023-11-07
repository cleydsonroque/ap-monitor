import sqlite3
from datetime import date

BD = 'ap.bd'
DATA = date.today()
DATA_FORMATADA = DATA.strftime('%d/%m/%Y')


class DataB():
    '''Implementa ORM parametrizado para manipular o BD das informações obtidas a partir do scraping dos anuncios dos imóveis.'''       

    def criar_conexão(self):
        self.con = sqlite3.connect(BD)
        self.cur = self.con.cursor()
    
    def encerrar_conexao(self):
        ''' Encerra a conexão com o BD'''
        self.con.close()

    def cria_tabela_bairro(self):
        ''' Caso não exista, cria uma tabela que recebe os dados do anuncio com os seguintes campos: 
            anuncio_id, cod_anuncio, imobiliaria, rua, bairro, cidade, metragem, quartos, vlr, vlr_com_tx, link_anuncio, criado_em e excluido_em.
        '''
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.bairro} (
                anuncio_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                cod_anuncio TEXT NOT NULL,
                imobiliaria TEXT NOT NULL,
                rua TEXT,
                bairro TEXT,
                cidade TEXT,
                metragem INTEGER,
                quartos INTEGER,
                vlr REAL,
                vlr_com_tx REAL,
                link_anuncio TEXT,
                criado_em TEXT,
                finalizado_em TEXT,
                UNIQUE(cod_anuncio)
                )                   
            ''')
        self.con.commit()

    def insere_dados(self, bairro='fonseca', dados=None):
        ''' Insere os dados na tabela a partir de uma lista de listas contendo uma tupla com os dados do anuncio:
            cod_anuncio, imobiliaria, rua, bairro, cidade, metragem, quartos, vlr, vlr_com_tx, link_anuncio e criado_em. 
        '''
        self.bairro = bairro
        self.anuncios = dados
        if len(self.anuncios) > 0:
            self.criar_conexão()
            self.cria_tabela_bairro()
            for anuncio in self.anuncios:   
                anuncio = [anuncio[0] + (DATA_FORMATADA,)]           
                try:
                    self.cur.executemany(f'''
                        INSERT INTO {self.bairro} (
                        cod_anuncio, 
                        imobiliaria, 
                        rua, 
                        bairro, 
                        cidade, 
                        metragem, 
                        quartos, 
                        vlr, 
                        vlr_com_tx, 
                        link_anuncio,
                        criado_em
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    ''', anuncio) 
                    self.con.commit()
                except: 
                    pass
            self.atualiza_finalizado()
            self.encerrar_conexao()

    # Atualiza o campo "finalizado_em" com a data do dia, caso o anuncio registrado anteriormente no banco foi finalizado
    def atualiza_finalizado(self):
        self.cur.execute(f'''SELECT * FROM {self.bairro} WHERE finalizado_em IS NULL;''')
        registros_bairro = [[l[1:11]] for l in self.cur.fetchall()]
        if len(registros_bairro) > 0:
            finalizados = [registro[0][0:2] for registro in registros_bairro if not registro in self.anuncios]
            if len(finalizados) > 0:
                for registro in finalizados:
                    registro = (DATA_FORMATADA,) + registro
                    self.cur.execute(f'''
                        UPDATE {self.bairro} 
                        SET finalizado_em = ? 
                        WHERE cod_anuncio = ? 
                        AND imobiliaria = ? 
                        ''', registro)
                    self.con.commit()

    def anunciado_hoje(self, bairro='fonseca'):
        self.criar_conexão()
        self.cur.execute(f'''SELECT * FROM {bairro} WHERE criado_em = '{DATA_FORMATADA}';''')
        hoje = [registro for registro in self.cur.fetchall()]
        self.encerrar_conexao()
        return hoje
    
    def anuncios_ativos(self, bairro='fonseca'):
        self.criar_conexão()
        self.cur.execute(f'''SELECT * FROM {bairro} WHERE finalizado_em IS NULL;''')
        ativo = [registro for registro in self.cur.fetchall()]
        self.encerrar_conexao()
        return ativo
    
    def anuncios_finalizados(self, bairro='fonseca'):
        self.criar_conexão()
        self.cur.execute(f'''SELECT * FROM {bairro} WHERE finalizado_em IS NOT NULL;''')
        finalizado = [registro for registro in self.cur.fetchall()]
        self.encerrar_conexao()
        return finalizado