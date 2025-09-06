import requests
import json
from datetime import datetime

def fetch_schedule():
    """
    Функция делает запрос к API МГУ и возвращает свежие данные расписания в виде словаря.
    """
    url = 'https://my.econ.msu.ru/Teacher/GetData'

    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://my.econ.msu.ru',
        'referer': 'https://my.econ.msu.ru/cacs',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': '__ddg1_=pLJWVzwrFIwCTqqeEfH8; _ym_uid=1753471215781307183; _ym_d=1753471215; MSU_GUEST_ID=50544595; MSU_LAST_VISIT=02.09.2025+00%3A15%3A54; _ga=GA1.2.46257710.1756761355; _ga_DH1EH9EZR2=GS2.2.s1756761355$o1$g0$t1756761355$j60$l0$h0; __RequestVerificationToken=R7CPcT16CVqb-yo_QMC4-GtLLoumLxrYpkWftY-2ONmPHHpn8ovh-jl7m9kfAvP67NLEhUHA68ZCIQYpo2FN_nA-SwffNfjEaXQaq91rcbY1; _ym_isad=2',
        '__requestverificationtoken': 'R7CPcT16CVqb-yo_QMC4-GtLLoumLxrYpkWftY-2ONmPHHpn8ovh-jl7m9kfAvP67NLEhUHA68ZCIQYpo2FN_nA-SwffNfjEaXQaq91rcbY1'
    }

    data = {
        'page': '1',
        'limit': '250', 
        'searchrasp[id]': '31561', 
        'searchrasp[label]': 'Корочкина Ульяна Сергеевна',
        'searchrasp[category]': 'Студенты',
        'searchrasp[value]': 'Корочкина Ульяна Сергеевна',
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()  # Возвращаем JSON-данные, а не пишем в файл
    except requests.exceptions.RequestException as e:
        print(f"Ошибка парсера: {e}")
        return {'records': []}  # Возвращаем пустой список при ошибке
