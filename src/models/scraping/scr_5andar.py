import requests
from parsel import Selector
from playwright.sync_api import sync_playwright
from time import sleep
# from datetime import date

TEXTO_CLASS_P_QTD_ENCONTRADA = 'CozyTypography'
TEXTO_SPAN_QTD_N_ENCONTRADA = 'Desenhar área de busca'
TEXTO_CLASS_H4_IMOVEL_N_ENCONTRADO = 'CozyTypography'
TEXTO_SPAN_IMOVEL_N_ENCONTRADO = 'Não encontramos'
TEXTO_HREF_URL_ANUNCIO = 'apartamento-'
TEXTO_DIV_GRID_CARD_RESULTADO = 'ROW_CARD'
IMOBILIARIA = 'QuintoAndar'
QTD_ELEMENTOS = 7
TEXTO_BTN_VER_MAIS = 'Ver mais'
# DATA = date.today()
# DATA_FORMATADA = DATA.strftime('%d/%m/%Y')
TEXTOS_PARA_REMOVER = [
    'Sem tempo para procurar?',
    'Saiba quando chegarem novos imóveis desta busca e a retome quando quiser',
    'Criar alerta de imóveis',
    'Novidade!',
    'Imóveis verificados e com ótima conservação'
    ]


class Scr5Andar():
    '''Retorna um conjunto de listas contendo as informaçoes dos apartamentos de 3 ou 4 quartos para alugar por bairro na cidade de Niterói - RJ, estraída do site da imobiliaria 5º Andar, conforme estrutura a seguir:

    [['cod_anuncio', 'imobiliaria', 'rua', 'bairro', 'cidade', 'metragem', 'quartos', 'vlr', 'vlr_com_tx', 'link_anuncio'],...]

    bairro padrão -> fonseca
    '''
    
    # Pega o html do resultado da busca pelo bairro pesquisado'''
    def __init__(self, bairro='fonseca'): 
        self._url = f'https://www.quintoandar.com.br/alugar/imovel/{bairro}-niteroi-rj-brasil/apartamento/3-4-quartos?referrer=profilingv2&flexible=true'
        self._html = requests.get(self._url).text
        self._sel = Selector(text=self._html)
        
    # Retorna a quantidade de anuncios encontrados
    def __qtd_anuncio__(self):
        html_p = self._sel.css(f'p[class*={TEXTO_CLASS_P_QTD_ENCONTRADA}]')
        _qtd_anuncio = html_p.css('span::text').get()
        html_h4 = self._sel.css(f'h4[class*={TEXTO_CLASS_H4_IMOVEL_N_ENCONTRADO}]')
        texto_alerta = html_h4.css('span::text').get()
        if TEXTO_SPAN_IMOVEL_N_ENCONTRADO not in texto_alerta and _qtd_anuncio != TEXTO_SPAN_QTD_N_ENCONTRADA:
            return int(_qtd_anuncio)
        else:
            return 0

    # Retorna uma lista com a url dos imóveis anunciados 
    def __url_anuncio__(self):  
        _url_anuncio = self._sel.css(f'a[href*={TEXTO_HREF_URL_ANUNCIO}]::attr(href)').getall()
        self._url_anuncio = _url_anuncio

    # Retorna uma lista com todas as informações dos imóveis
    def __info_anuncio__(self):
        html_div = self._sel.css(F'div[data-testid*={TEXTO_DIV_GRID_CARD_RESULTADO}]')
        _info_anuncio = html_div.css('span::text').getall()
        _info_anuncio = [e for e in _info_anuncio if e not in TEXTOS_PARA_REMOVER]
        self._info_anuncio = _info_anuncio

    # Realiza o tratamento dos dados de saída e retorna em uma lista.
    def __tratamento_dados__(self):
        info_anuncio = self._info_anuncio
        url_anuncio = self._url_anuncio
        if len(info_anuncio)/len(url_anuncio) == QTD_ELEMENTOS:
            info_anuncio = [info_anuncio[e:e+QTD_ELEMENTOS] for e in range(0, len(info_anuncio), QTD_ELEMENTOS)]
            _dados = [info_anuncio[e] + [url_anuncio[e]] for e in range(0, len(info_anuncio))]
            for imovel in _dados:
                imovel.insert(0, imovel[7][38:47])  
                imovel[1] = IMOBILIARIA # imobiliaria
                imovel.insert(3, imovel[3][:imovel[3].find(',')]) # bairro
                imovel[4] = imovel[4][imovel[4].find(',')+2:] # cidade   
                imovel[5] = int(imovel[5][:imovel[5].find(' ')]) # metragem
                imovel[6] = int(imovel[6][:imovel[6].find(' ')]) # quartos
                imovel[7] = int(imovel[7][imovel[7].find('R')+3:].replace('.','')) # vlr
                imovel[8] = int(imovel[8][imovel[8].find('R')+3:].replace('.','')) # vlr_com_tx
                # imovel.append(DATA_FORMATADA) # criado_em
            _dados = [[tuple(e)] for e in _dados]
        
            return _dados
    
    # Inilicializa um navegador e carrega a url
    def __navegador__(self):
        self._pw = sync_playwright().start()
        self._browser = self._pw.firefox.launch()
        self._page = self._browser.new_page()
        self._page.goto(self._url)
        sleep(2)
        # return(_page, _browser, _pw)

    # Finaliza o navegador
    def __fecha_navegador__(self):
        self._browser.close()
        self._pw.stop()

    # Clica no botão 'Ver mais'
    def __click__(self):
        self._page.get_by_label(TEXTO_BTN_VER_MAIS).click()
        sleep(2)   

    # Retorna false caso não encontre o texto 'Ver mais' na página
    def __tem_vermais__(self):
        if TEXTO_BTN_VER_MAIS in self._html:
            return (True)
        else: return(False)

    # Retorna o html da pagina e estancia o seletor
    def __str_html__(self):
        self._html = self._page.content()
        self._sel = Selector(text=self._html)
    
    def saida(self):
        if self.__tem_vermais__():
            self.__navegador__()
            while True:
                self.__click__()
                self.__str_html__()
                if not self.__tem_vermais__():
                    break
            self.__fecha_navegador__()
            self.__url_anuncio__()
            self.__info_anuncio__()
            dados = self.__tratamento_dados__()
            return (dados)
        elif self.__qtd_anuncio__() == 0:
            return ([])
        else:
            self.__url_anuncio__()
            self.__info_anuncio__()
            dados = self.__tratamento_dados__()
            return (dados)
        
# print(Scr5Andar(bairro='piratininga').saida())