import requests
from parsel import Selector


# Retorna o html do resultado da busca pelo bairro pesquisado.
BAIRRO = 'fonseca'
URL = f'https://www.quintoandar.com.br/alugar/imovel/{BAIRRO}-niteroi-rj-brasil/apartamento/3-4-quartos?referrer=profilingv2&flexible=true'
html = requests.get(URL).text
sel = Selector(text=html)

# Retorna True quando não encontra imóveis
TEXTO_CLASS_H4_N_ENCONTRADO = 'CozyTypography'
html_h4 = sel.css(f'h4[class*={TEXTO_CLASS_H4_N_ENCONTRADO}]')
alerta = html_h4.css('span::text').get()
if 'encontramos' in alerta:
    print(alerta)

# Retorna a quantidade de imóveis encontrados
TEXTO_CLASS_P_QTD_ENCONTRADA = 'CozyTypography'
html_p = sel.css(f'p[class*={TEXTO_CLASS_P_QTD_ENCONTRADA}]')
quantidade = html_p.css('span::text').get()
if not 'alerta' in quantidade:
    print(quantidade)

# Retorna uma lista com a url do anuncio do imóvel.   
TEXTO_COMUM_URL_ANUNCIO = f'apartamento-'
url_anuncio = sel.css(f'a[href*={TEXTO_COMUM_URL_ANUNCIO}]::attr(href)').getall()

# Retorna uma lista com as informações do imóvel.
TEXTO_DIV_GRID_CARD_RESULTADO = 'ROW_CARD'
html_div = sel.css(F'div[data-testid*={TEXTO_DIV_GRID_CARD_RESULTADO}]')
info_anuncio = html_div.css('span::text').getall()

# Realiza o tratamento dos dados de saída e retorna em uma lista.
IMOBILIARIA = 'QuintoAndar'
QTD_ELEMENTOS = 7
if len(info_anuncio)/len(url_anuncio) == QTD_ELEMENTOS:
    info_anuncio = [info_anuncio[e:e+QTD_ELEMENTOS] for e in range(0, len(info_anuncio), QTD_ELEMENTOS)]
    dados = [info_anuncio[e] + [url_anuncio[e]] for e in range(0, len(info_anuncio))]
    for imovel in dados:
        imovel.insert(0, imovel[7][38:47])
        imovel[1] = IMOBILIARIA
        imovel.insert(3, imovel[3][:imovel[3].find(',')])
        imovel[4] = imovel[4][imovel[4].find(',')+2:]   
        imovel[5] = imovel[5][:imovel[5].find(' ')]
        imovel[6] = imovel[6][:imovel[6].find(' ')]
        imovel[7] = imovel[7][imovel[7].find('R')+3:].replace('.','')
        imovel[8] = imovel[8][imovel[8].find('R')+3:].replace('.','')
    print(dados)
else:
    print('Rever a lógica que lista as informações do anuncio (linhas 17 a 19)')