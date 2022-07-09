import pandas as pd
import requests
from faker import Faker
from flask import Flask, jsonify
from http import HTTPStatus
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, abort

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
        columns_data[column_name] = [columns_data[column_name]() for _ in range(count)] if column_name != 'birthday' \
            else [fake_inst.date_of_birth(minimum_age=18, maximum_age=45) for _ in range(count)]

    # 1 option. Transformation fake data to Panda's dataframe object and turn it into html
    # students_table = pd.DataFrame(columns_data).to_html()
    # return f"<p>{students_table}</p>"

    # 2 option. Creating csv file with fake data,reading csv to turn it into html
    with open("students_csv.csv", "w") as file:
        file.write(pd.DataFrame(columns_data).to_csv(index=False))

    file = pd.read_csv("students_csv.csv")
    students_table = file.to_html()
    return f"<p>{students_table}</p>"


@app.route("/bitcoin_rate")
@use_kwargs(
    {
        "currency_code": fields.Str(load_default="USD"),
        "count": fields.Int(required=True,
                            validate=[validate.Range(min=1)])
    },
    location="query"
)
def get_bitcoin_value(currency_code, count):
    currency_code = currency_code.upper()
    currencies = requests.get("https://bitpay.com/currencies").json().get('data')
    available_currency_codes = [currency['code'] for currency in currencies]
    validate_currency(available_currency_codes, currency_code)
    bitpay_currency = requests.get(url='https://bitpay.com/rates/BTC/' + currency_code).json().get('data')
    currency_rate = bitpay_currency.get('rate')

    # Currency symbol parsing
    symbol = next(
        bitpay_currency['symbol'] for bitpay_currency in currencies if bitpay_currency['code'] == currency_code
    )

    return f"<p> Current BTC exchange rate is {currency_rate} {currency_code} {symbol} per 1 bitcoin </p>" \
           f"<p> For {count} BTC will cost you {round(count * currency_rate, 2)} {symbol}</p>"


def validate_currency(available, requested):
    if requested not in available:
        raise abort(400, messages=[f'Wrong currency code. Available codes: {available}'])


if __name__ == "__main__":
    app.run(debug=True)
