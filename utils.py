import requests
import json
from config import keys



class ConversionException(Exception):
    pass

class CryptoConventer:
    @staticmethod
    def convert(quoats: str, base: str, amount: str):
        if quoats == base:
            raise ConversionException(f"Невозможно перевести одинаковые валюты {base}")

        try:
            quoats_ticker = keys[quoats]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {quoats}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f"Не удалось обработать количество {amount}")
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quoats_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
