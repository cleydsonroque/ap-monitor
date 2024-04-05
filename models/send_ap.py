import requests
TOKEN = '6392370895:AAETTDJBu5ZfBom0tRf7Ii_3ZjpHwlL8PhQ'
CHAT_ID = -4108344840


def to_send(anuncios):
    if len(anuncios) > 0: 
        for ap in anuncios:
            text_msg = f'Anuncio postado em {ap[13]}, {ap[10]}.\n\n{ap[12]}'
            url_send_msg = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text_msg}'
            requests.get(url_send_msg)