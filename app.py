from models.scraping.scr_5andar import Scr5Andar
from models.scr_orm import DataB
from models.send_ap import to_send


bairros = ['piratininga', 'barreto', 'fonseca', 'icarai', 'centro']
for bairro in bairros:
    lista = Scr5Andar(bairro=bairro).saida()
    bd = DataB()
    bd.insere_dados(bairro=bairro, dados=lista)
    anuncios = bd.anunciado_hoje(bairro=bairro)
    to_send(anuncios)