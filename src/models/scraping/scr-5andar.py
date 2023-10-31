import requests
from parsel import Selector
from playwright.sync_api import sync_playwright
from time import sleep


# Retorna o html do resultado da busca pelo bairro pesquisado.
BAIRRO = 'fonseca'
URL = f'https://www.quintoandar.com.br/alugar/imovel/{BAIRRO}-niteroi-rj-brasil/apartamento/3-4-quartos?referrer=profilingv2&flexible=true'
html = requests.get(URL).text
sel = Selector(text=html)

# Retorna a quantidade de imóveis encontrados
def qtd(sel):
    TEXTO_CLASS_P_QTD_ENCONTRADA = 'CozyTypography'
    TEXTO_CLASS_H4_N_ENCONTRADO = 'CozyTypography'
    html_p = sel.css(f'p[class*={TEXTO_CLASS_P_QTD_ENCONTRADA}]')
    qtd_anuncio = html_p.css('span::text').get()
    html_h4 = sel.css(f'h4[class*={TEXTO_CLASS_H4_N_ENCONTRADO}]')
    texto_alerta = html_h4.css('span::text').get()
    if 'encontramos' not in texto_alerta and qtd_anuncio != 'Desenhar área de busca':
        return(int(qtd_anuncio))
    else:
        return(0)

# Retorna uma lista com a url do anuncio do imóvel. 
def url(sel):  
    TEXTO_COMUM_URL_ANUNCIO = f'apartamento-'
    url_anuncio = sel.css(f'a[href*={TEXTO_COMUM_URL_ANUNCIO}]::attr(href)').getall()
    return(url_anuncio)

# Retorna uma lista com as informações do imóvel.
def imovel(sel):
    TEXTO_DIV_GRID_CARD_RESULTADO = 'ROW_CARD'
    html_div = sel.css(F'div[data-testid*={TEXTO_DIV_GRID_CARD_RESULTADO}]')
    info_anuncio = html_div.css('span::text').getall()
    REMOVE_LIST = [
        'Sem tempo para procurar?',
        'Saiba quando chegarem novos imóveis desta busca e a retome quando quiser',
        'Criar alerta de imóveis',
        'Novidade!',
        'Imóveis verificados e com ótima conservação'
    ]
    info_anuncio = [e for e in info_anuncio if e not in REMOVE_LIST]
    return(info_anuncio)

# Realiza o tratamento dos dados de saída e retorna em uma lista.
def saida(info_anuncio, url_anuncio):
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
        return(dados)
   
# Inilicializa um navegador e carrega a url
def navegador(URL):
    pw = sync_playwright().start()
    browser = pw.firefox.launch()
    page = browser.new_page()
    page.goto(URL)
    sleep(2)
    return(page, browser, pw)

# Finaliza o navegador
def fecha_nav(browser, pw):
    browser.close()
    pw.stop()

# Clica no botão 'Ver mais'
def click(pagina):
    pagina.get_by_label("Ver mais").click()
    sleep(2)   

# Retorna fause cas não encontre o texto 'Ver mais' na página
def tem_vermais(html):
    if 'Ver mais' in html:
        return (True)
    else: return(False)

# Retorna o html da pagina e estancia o seletor
def str_html(pagina):
    html = pagina.content()
    sel = Selector(text=html)
    return(html, sel)

print(f'\nFoi listado {qtd(sel)} imoveis\n')
if tem_vermais(html):
    page, browser, pw = navegador(URL)
    while True:
        click(page)
        html = str_html(page)[0]
        if not tem_vermais(html):
            break
    sel = str_html(page)[1]
    fecha_nav(browser, pw)
    dados = saida(imovel(sel), url(sel))
    print(dados)
elif qtd(sel) == 0:
    print('Não há imóveis\n')
else: 
    dados = saida(imovel(sel), url(sel))
    print(dados)
