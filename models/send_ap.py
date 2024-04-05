import requests


def to_send(anuncios, token, chat_id):
    if len(anuncios) > 0: 
        for ap in anuncios:
            text_msg = f'Anuncio postado em {ap[13]}, {ap[10]}.\n\n{ap[12]}'
            url_send_msg = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text_msg}'
            requests.get(url_send_msg)