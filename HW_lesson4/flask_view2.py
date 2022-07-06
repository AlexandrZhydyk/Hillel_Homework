import pandas as pd
import requests
import json
# Import currency code array for input validation
from Currency_code_request import currency_code_arr
from faker import Faker
from flask import Flask, jsonify
from http import HTTPStatus
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


@app.errorhandler(HTTPStatus.BAD_REQUEST)
@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
def error_handler(error):
    print(type(error))
    headers = error.data.get("headers", None)
    print(headers)
    messages = error.data.get("messages", ["Invalid request."])
    print(messages)
    if headers:
        return jsonify({
            "errors": messages
            },
            error.code,
            headers
        )
    else:
        return jsonify({
            "errors": messages
            },
            error.code)


@app.route("/")
@use_kwargs(
    {
        "count": fields.Int(required=True,
                            validate=[validate.Range(min=1, max=1000)],
                            ),
    },
    location="query"
)
def generate_students(count):
    fake_inst = Faker("UK")
    # A dict for creating fake data
    columns_data = {"first_name": fake_inst.first_name, "last_name": fake_inst.last_name, "email": fake_inst.email,
            "birthday": None, "password": fake_inst.password}
    # Fake data creation
    for column_name in columns_data:
        columns_data[column_name] = [columns_data[column_name]() for _ in range(count)] if column_name != 'birthday'\
            else [fake_inst.date_of_birth(minimum_age=18, maximum_age=45) for _ in range(count)]

    # 1 option. Transformation fake data to Panda's dataframe object and turn it into html
    # students_table = pd.DataFrame(columns_data).to_html()
    # return f"<p>{students_table}</p>"

    #2 option. Creating csv file with fake, reading csv to turn it into html
    with open("students_csv.csv", "w") as file:
        file.write(pd.DataFrame(columns_data).to_csv(index=False))

    file = pd.read_csv("students_csv.csv")
    students_table = file.to_html()
    return f"<p>{students_table}</p>"


@app.route("/bitcoin_rate")
@use_kwargs(
    {
        "currency_code": fields.Str(load_default="USD",
                                    validate=[validate.OneOf(currency_code_arr, error="Enter a currency code. Ex.: USD for US dollar, UAH for grivnya")]),
        "count": fields.Int(required=True,
                            validate=[validate.Range(min=1)])
    },
    location="query"
)
def get_bitcoin_value(currency_code, count):
    # Exchange rate parsing
    resource_url = 'https://bitpay.com/rates/BTC/'
    headers = {'X-Accept-Version': '2.0.0', 'Content-type': 'application/json'}
    response = requests.get(url=resource_url + currency_code, headers=headers).content
    dict_response = json.loads(response)
    currency_rate = dict_response['data'].get('rate')

    # Currency symbol parsing
    resource_url = 'https://test.bitpay.com/currencies'
    headers = {'X-Accept-Version': '2.0.0', 'Content-type': 'application/json'}
    response = requests.get(url=resource_url, headers=headers).content
    currencies_dict = json.loads(response)
    symbol = ""
    for currency in currencies_dict['data']:
        if currency['code'] == currency_code:
            symbol += currency['symbol']

    return f"<p> Current BTC exchange rate is {currency_rate} {currency_code} {symbol} per 1 bitcoin </p>"\
        f"<p> For {count} {currency_code} you can buy {count/currency_rate} BTC</p>"


if __name__ == "__main__":
    app.run()
