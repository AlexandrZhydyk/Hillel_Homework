import pandas as pd

from flask import Flask, jsonify
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs, abort

from database_handler import query_handler, get_column_names


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


@app.route('/stats_by_city')
@use_kwargs(
    {
        "genre": fields.Str(required=True),
    },
    location="query"
)
def get_city_fan(genre):

    # Make input key insensitive
    query_available_genres = "SELECT DISTINCT Name AS Genre FROM genres "
    available_genres = query_handler(query_available_genres)
    data_available_genres = {}
    for available_genre in available_genres:
        data_available_genres[str(available_genre[0]).lower()] = str(available_genre[0])
    genre = str(genre).lower()

    if genre not in data_available_genres:
        formatted_available_genres = [available_genre[0] for available_genre in available_genres]
        raise abort(400, messages=[f'Wrong country name. Please check available countries: {formatted_available_genres}'])
    else:
        query = "SELECT genres.Name AS Genre, City, COUNT(CustomerId) AS CustomerQty " \
                "FROM customers " \
                "JOIN invoices USING (CustomerId)" \
                "JOIN invoice_items USING (InvoiceId)" \
                "JOIN tracks USING (TrackId)" \
                "JOIN genres USING (GenreId)" \
                "GROUP BY Genre, City " \
                f"HAVING Genre == '{data_available_genres[genre]}' " \
                "ORDER BY CustomerQty DESC " \
                "LIMIT 1"
    return response_to_html_view(query)




def response_to_html_view(query):
    all_data = query_handler(query)
    columns_name = get_column_names(query)
    return (pd.DataFrame(all_data, columns=columns_name)).to_html()



if __name__ == "__main__":

    app.run(port=5001)