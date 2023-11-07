from models.scraping.scr_5andar import Scr5Andar
from models.scr_orm import DataB


bairros = ['piratininga', 'barreto', 'fonseca', 'icarai', 'centro']
for bairro in bairros:
    lista = Scr5Andar(bairro=bairro).saida()
    bd = DataB()
    bd.insere_dados(bairro=bairro, dados=lista)
    ativos = bd.anuncios_ativos(bairro=bairro)
    print(f'{bairro}: {len(ativos)} imóveis anunciados')