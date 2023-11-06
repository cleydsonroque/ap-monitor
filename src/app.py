from models.scraping.scr_5andar import Scr5Andar
from models.scr_orm import DataB


bairros = ['piratininga', 'barreto', 'fonseca', 'icarai', 'centro']
for bairro in bairros:
    lista = Scr5Andar(bairro=bairro).saida()
    bd = DataB()
    bd.insere_dados(bairro=bairro, dados=lista)

# for bairro in bairros:
#     bd = DataB()
    ativos = bd.anuncios_ativos(bairro=bairro)
    print(f'{bairro}: {len(ativos)} imóveis anunciados')
    finalizados = bd.anuncios_finalizados(bairro=bairro)
    print(f'{bairro}: {len(finalizados)} imóveis finalizados')
    anuncios = bd.anunciado_hoje(bairro=bairro)
    print(f'{bairro}: {len(anuncios)} imóveis anunciados hoje')
    # for ativo in ativos:
    #     print(ativo[10])
    # for finalizado in finalizados:
    #     print(finalizado[10])