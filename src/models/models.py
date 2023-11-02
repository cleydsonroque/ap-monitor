import sqlite3
from scraping import scr_5andar

BD = 'ap.db'

class DataB():
    '''Manipula o banco de dados'''

    # Cria uma conexão com o banco e estancia o cursor
    def __init__(self):
        self.con = sqlite3.connect(BD)
        self.cur = self.con.cursor()
    
    # Encerra a conexão
    def encerrar_conexao(self):
        self.con.close()

    # 'cod_anuncio', 'imobiliaria', 'rua', 'bairro', 'cidade', 'metragem', 'quartos', 'vlr', 'vlr_com_tx', 'link_anuncio', 'criado_em', 'ultima_consulta']
    def cria_tabela(self):
        self.cur.executescript('''
            CREATE TABLE IF NOT EXISTS anuncios(
                anuncio_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                cod_anuncio TEXT NOT NULL,
                imobiliaria TEXT NOT NULL,
                rua TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                metragem INTEGER NOT NULL,
                quartos INTEGER NOT NULL,
                vlr REAL NOT NULL,
                vlr_com_tx REAL NOT NULL,
                link_anuncio TEXT NOT NULL,
                criado_em TEXT NOT NULL
                )                   
            ''')
        self.con.commit()

    # Insere os dados na tabela a partir de uma lista
    def insere_dados(self, lista):
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
            ''', lista)
        self.con.commit()
  
if __name__ == '__main__':
    lista = scr_5andar.Scr5Andar(bairro='barreto').saida()
    db = DataB()
    db.cria_tabela()
    db.insere_dados(lista)
    db.encerrar_conexao()
    