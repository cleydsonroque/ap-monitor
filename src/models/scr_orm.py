import sqlite3
from scraping import scr_5andar
from datetime import date

BD = 'ap.db'
DATA = date.today()
DATA_FORMATADA = DATA.strftime('%d/%m/%Y')


class DataB():
    '''Implementa ORM parametrizado para manipular o BD das informações obtidas a partir do scraping dos anuncios dos imóveis.'''

    # Cria uma conexão com o banco e estancia o cursor
    def __init__(self):
        self.con = sqlite3.connect(BD)
        self.cur = self.con.cursor()
    
    def encerrar_conexao(self):
        ''' Encerra a conexão com o BD'''
        self.con.close()

    def cria_tabela_anuncios(self):
        ''' Caso não exista, cria uma tabela que recebe os dados do anuncio com os seguintes campos: 
            anuncio_id, cod_anuncio, imobiliaria, rua, bairro, cidade, metragem, quartos, vlr, vlr_com_tx, link_anuncio, criado_em e excluido_em.
        '''
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS anuncios(
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
                excluido_em TEXT,
                UNIQUE(cod_anuncio)
                )                   
            ''')
        self.con.commit()

    def insere_dados(self, lista):
        ''' Insere os dados na tabela a partir de uma lista de listas contendo uma tupla com os dados do anuncio:
            cod_anuncio, imobiliaria, rua, bairro, cidade, metragem, quartos, vlr, vlr_com_tx, link_anuncio e criado_em. 
        '''
        for anuncio in lista:   
            anuncio = [anuncio[0] + (DATA_FORMATADA,)]           
            try:
                self.cur.executemany('''
                    INSERT INTO anuncios (
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

    # verifica se o anuncio registrado no banco consta na lista
    def anuncio_ativo(self):
        lista = [
            [('893586005', 'QuintoAndar', 'Rua Fagundes Varela', 'Piratininga', 'Niterói', 220, 3, 7750, 10460, 'https://www.quintoandar.com.br/imovel/893586005/alugar/apartamento-3-quartos-piratininga-niteroi')],
            [('893552226', 'QuintoAndar', 'Rua Marechal Raul de Albuquerque', 'Piratininga', 'Niterói', 173, 4, 5500, 8943, 'https://www.quintoandar.com.br/imovel/893552226/alugar/apartamento-4-quartos-piratininga-niteroi')],
            [('893511216', 'QuintoAndar', 'Rua Itapuca', 'Piratininga', 'Niterói', 434, 5, 5250, 8778, 'https://www.quintoandar.com.br/imovel/893511216/alugar/apartamento-5-quartos-piratininga-niteroi')]
            ]
        self.cur.execute('''SELECT * FROM anuncios;''')
        bd = [[l[1:11]] for l in self.cur.fetchall()]
        # print (bd - lista)
        for r in bd:
            print(r)
            if not r in lista:
                # print(r[1])
                print(r[0][0])
        # print(bd)

if __name__ == '__main__':
    lista = scr_5andar.Scr5Andar(bairro='piratininga').saida()
    # print(lista)
    # lista = [
    #     [('893464293', 'QuintoAndar', 'Rua Doutor Luiz Palmier', 'Barreto', 'Niterói', 67, 3, 2600, 3415, 'https://www.quintoandar.com.br/imovel/893464280/alugar/apartamento-3-quartos-barreto-niteroi', '03/11/2023')],
    #     [('894198724', 'QuintoAndar', 'Rua Doutor Luiz Palmier', 'Barreto', 'Niterói', 73, 3, 2500, 3417, 'https://www.quintoandar.com.br/imovel/894198709/alugar/apartamento-3-quartos-barreto-niteroi', '03/11/2023')]
    #     ]
    # print(lista)
    db = DataB()
    # db.cria_tabela_anuncios()
    # db.insere_dados(lista)
    db.anuncio_ativo()
    db.encerrar_conexao()
    