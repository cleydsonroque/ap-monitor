from models.scraping.scr_5andar import Scr5Andar
from models.scr_orm import DataB


bairros = ['piratininga', 'fonseca', 'barreto']
for bairro in bairros:
    lista = Scr5Andar(bairro=bairro).saida()
    DataB(bairro=bairro, dados=lista)