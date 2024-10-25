from typing import Optional

import requests


def get_dollar_currency() -> tuple[Optional[float], bool]:
    url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for currency in data:
            if currency['Ccy'] == 'USD':
                usd_rate = float(currency['Rate'])
                return usd_rate, True
    return None, False

def convert_price(price, currency='USD'):
    exchange_rates = {
        'USD': 1,
        'EUR': 0.85,
        'UZS': 11500,  # Masalan, 1 USD = 11500 UZS
    }
    return price * exchange_rates.get(currency, 1)