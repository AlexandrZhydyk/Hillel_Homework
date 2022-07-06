import pandas as pd

from http import HTTPStatus

from faker import Faker
from flask import Flask, jsonify
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

app = Flask(__name__)

@app.errorhandler(HTTPStatus.BAD_REQUEST)
@app.errorhandler(422)
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
    fake_data = Faker("UK")
    # count = int(request.args.get('count'))
    data = {"first_name": fake_data.first_name, "last_name": fake_data.last_name, "email": fake_data.email,
            "birthday": None, "password": fake_data.password}
    for column_name in data:
        data[column_name] = [data[column_name]() for _ in range(count)] if column_name != 'birthday'\
            else [fake_data.date_of_birth(minimum_age=18, maximum_age=45) for _ in range(count)]
    # students_table = pd.DataFrame(data).to_csv(index=False)

    with open("students_csv.csv", "w") as file:
        file.write(pd.DataFrame(data).to_csv(index=False))

    file = pd.read_csv("students_csv.csv")
    students_table = file.to_html()
    return f"<p>{students_table}</p>"


app.run()