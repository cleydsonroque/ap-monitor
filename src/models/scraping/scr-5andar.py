import requests
from parsel import Selector


# Retorna o html do resultado da busca pelo bairro pesquisado.
BAIRRO = 'fonseca'
URL = f'https://www.quintoandar.com.br/alugar/imovel/{BAIRRO}-niteroi-rj-brasil/apartamento/3-4-quartos?referrer=profilingv2&flexible=true'
html = requests.get(URL).text
sel = Selector(text=html)

# Retorna uma lista com a url do anuncio do imóvel.   
TEXTO_COMUM_URL_ANUNCIO = f'quartos-{BAIRRO}-niteroi'
url_anuncio = sel.css(f'a[href*={TEXTO_COMUM_URL_ANUNCIO}]::attr(href)').getall()

# Retorna uma lista com as informações do imóvel.
TEXTO_DIV_GRID_CARD_RESULTADO = 'ROW_CARD'
html_div = sel.css(F'div[data-testid*={TEXTO_DIV_GRID_CARD_RESULTADO}]')
dados_anuncio = html_div.css('span::text').getall()

# Realiza o tratamento dos dados de saída
IMOBILIARIA = 'QuintoAndar'
REMOVE_LIST = ['Apartamento', f'{BAIRRO.capitalize()}, Niterói']
dados_anuncio = [e for e in dados_anuncio if e not in REMOVE_LIST]
dados_anuncio = [dados_anuncio[e:e+5] for e in range(0, len(dados_anuncio), 5)]
dados = [[IMOBILIARIA] + dados_anuncio[e] + [url_anuncio[e]] for e in range(0, len(dados_anuncio))]
for imovel in dados:
    imovel[2] = imovel[2][:imovel[2].find(' ')]
    imovel[3] = imovel[3][:imovel[3].find(' ')]
    imovel[4] = imovel[4][imovel[4].find('R')+3:].replace('.','')
    imovel[5] = imovel[5][imovel[5].find('R')+3:].replace('.','')
    imovel.insert(0, imovel[6][38:47])

print(dados)
