import requests
import json

from config import cur_list, exrates_token


class ExRatesAPI:

    @staticmethod
    def get_price(base, quote, amount):
        r = requests.get(
            f'http://api.exchangeratesapi.io/v1/latest?access_key={exrates_token}&&symbols={",".join(cur_list.values())}&format=1')
        text = json.loads(r.text)
        return float(text['rates'][quote]) / float(text['rates'][base]) * amount


class APIException(BaseException):
    pass