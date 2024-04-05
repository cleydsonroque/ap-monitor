import requests
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from time import sleep


TEXTO_SPAN_IMOVEL_N_ENCONTRADO = 'Não encontramos'
TEXTO_BTN_VER_MAIS = 'Ver mais'
NOME_ATRIBUTO = 'data-testid'
VLR_ATRIBUTO_QTD_ENCONTRADA = 'CONTEXTUAL_SEARCH_TITLE'
TEXTO_HREF_URL_ANUNCIO = 'apartamento-'
QTD_ELEMENTOS = 9
IMOBILIARIA = 'QuintoAndar'


class Scr5Andar():
    '''Retorna um conjunto de listas contendo as informaçoes dos apartamentos de 3 ou 4 quartos para alugar
    por bairro na cidade de Niterói - RJ, estraída do site da imobiliaria 5º Andar, conforme estrutura a seguir:
    [['cod_anuncio', 'imobiliaria', 'rua', 'bairro', 'cidade', 'metragem', 'quartos', 'vlr', 'vlr_com_tx',
    'link_anuncio'],...] bairro padrão -> fonseca
    '''
    
    # Pega o html do resultado da busca pelo bairro pesquisado'''
    def __init__(self, bairro='fonseca'): 
        self._url = f'https://www.quintoandar.com.br/alugar/imovel/{bairro}-niteroi-rj-brasil/apartamento/3-4-quartos?referrer=profilingv2&flexible=true'
        html = requests.get(self._url).text
        self._html = BeautifulSoup(html, 'html.parser')
        self._dados = []
        self._cont_click = -1
               

    # Retorna False caso não tenha anuncio
    def __tem_anuncio__(self):
        texto_alerta = self._html.h4.span.text 
        if TEXTO_SPAN_IMOVEL_N_ENCONTRADO in texto_alerta:
            return False
        return True
    

    # Retorna False caso não encontre o texto 'Ver mais' na página
    def __tem_vermais__(self):
        if TEXTO_BTN_VER_MAIS in self._html.text:
            return True
        return False

   
    # Retorna a quantidade de anuncios encontrados
    def __qtd_anuncio__(self):
        qtd_anuncio = self._html.find(attrs={NOME_ATRIBUTO:VLR_ATRIBUTO_QTD_ENCONTRADA}).span.text
        return int(qtd_anuncio)
    

    # Retorna uma lista com a url dos imóveis anunciados 
    def __url_anuncio__(self):  
        tag_a = self._html.find_all('a')
        urls = [tag['href'] for tag in tag_a if 'href' in tag.attrs]
        url_anuncio = [url for url in urls if TEXTO_HREF_URL_ANUNCIO in url] 
        return url_anuncio


    # Retorna uma lista com todas as informações dos imóveis 
    def __info_anuncio__(self):
        tag_h2_h3 = self._html.find_all(re.compile('^h[2-3]'))
        info_anuncio = [tag.text for tag in tag_h2_h3]
        return info_anuncio


    # Realiza o tratamento dos dados de saída e retorna em uma lista.
    def __agrupa_anuncio__(self):
        info_anuncio = self.__info_anuncio__()
        url_anuncio = self.__url_anuncio__()
        lista_info = []
        for info in info_anuncio:
            novo_valor = re.split(r'[·,]', info) # Ex. caracter "·····"
            if len(novo_valor) == 2:
                novo_valor.append('0 vaga')
            novo_valor = [item.strip() for item in novo_valor]
            lista_info.extend(novo_valor)
        # print(f'qtd info: {len(lista_info)}')
        # print(f'qtd url: {len(url_anuncio)}')
        # print(len(lista_info)/len(url_anuncio))
        if len(lista_info)/len(url_anuncio) == QTD_ELEMENTOS:
            info_anuncio = [lista_info[e:e+QTD_ELEMENTOS] for e in range(0, len(lista_info), QTD_ELEMENTOS)]
            dados_anuncio = [info_anuncio[e] + [url_anuncio[e]] for e in range(0, len(info_anuncio))]
            self.dados_anuncio = dados_anuncio
            return True
        else:
            self.dados_anuncio = []
            return False


    # Realiza o tratamento dos dados de saída e retorna em uma lista.
    def __trata_dados__(self):
        dados = self.dados_anuncio
        for imovel in dados:
            imovel.insert(0, IMOBILIARIA)
            imovel.insert(0, imovel[10][38:47])  
            imovel[3] = int(imovel[3][imovel[3].find('$')+2:imovel[3].find('total')-1].replace('.','')) # vlr_com_tx
            imovel[4] = int(imovel[4][imovel[4].find('$')+2:imovel[4].find('aluguel')-1].replace('.','')) # vlr_sem_tx
            imovel[5] = int(imovel[5][:imovel[5].find('m')-1]) # metragem
            imovel[6] = int(imovel[6][:imovel[6].find('q')-1]) # quartos
            imovel[7] = int(imovel[7][:imovel[7].find('v')-1]) # vagas
            if not imovel in self._dados:
                self._dados.append(imovel)
    

    # Retorna o json com os dados do anuncio
    def __check_json(self, response):
        if 'search/coordinates' in response.url:
            self.trata_json(response.json())


    # Inilicializa um navegador e carrega a url
    def __navegador__(self):
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=True)
        self._page = self._browser.new_page()
        self._page.set_viewport_size(
            {'width': 1200, 'height': 600}
            )
        sleep(3)
        # self._page.on('response', lambda response: self.__check_json(response))
        self._page.goto(self._url)
        sleep(2)


    # Clica no botão 'Ver mais'
    def __click__(self):
        self._page.get_by_label(TEXTO_BTN_VER_MAIS).click()
        self._page.wait_for_load_state('networkidle')
        self._cont_click = self._cont_click + 1
        sleep(5)


    # Instancia o html da pagina atual
    def __str_html__(self):
        html = self._page.content()
        self._html = BeautifulSoup(html, 'html.parser')


    # Finaliza o navegador
    def __fecha_navegador__(self):
        # self._page.keyboard.press('Home')
        # self._page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        # self._page.keyboard.press('End')
        sleep(2)   
        self._browser.close()
        self._pw.stop()


    # Trata json
    def trata_json(self, dados_json):
        hits = dados_json['hits']['hits']
        print(len(hits))
        for anuncio in hits:
            print(anuncio['_source']['id'])


    # Retorna lista de anuncios formatada conforme input padrão do BD
    def saida(self):
        if not self.__tem_anuncio__():
            return []
        if self.__tem_vermais__():
            qtd_anuncio = self.__qtd_anuncio__()
            self.__navegador__()
            while True:
                for i in range(3):
                    if self.__agrupa_anuncio__():
                        break
                self.__trata_dados__()
                self.__click__()
                self.__str_html__()
                if not self.__tem_vermais__():
                    break
                if self._cont_click > qtd_anuncio // 10:
                    self._cont_click = -1
                    break
            self.__fecha_navegador__()
        for i in range(3):
            if self.__agrupa_anuncio__():
                break
        self.__trata_dados__()
        return [[tuple(e)] for e in self._dados]