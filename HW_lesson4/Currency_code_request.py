import requests
import json


def get_currency_code_arr():
    resource_url = 'https://bitpay.com/currencies'
    headers = {'X-Accept-Version': '2.0.0', 'Content-type': 'application/json'}
    response = requests.get(url=resource_url, headers=headers).content
    dict_response = json.loads(response)
    currency_arr = []
    for currency in dict_response['data']:
        currency_code_arr.append(currency["code"])
    return currency_arr


currency_code_arr = get_currency_code_arr()
print(currency_code_arr)


