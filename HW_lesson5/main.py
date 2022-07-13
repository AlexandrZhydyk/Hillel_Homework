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


@app.route('/sales')
@use_kwargs(
    {
        "country": fields.Str(load_default=None),
    },
    location="query"
)
def order_price(country):
    if country is None:
        country = ""
    else:
        country = str(country).lower()
    # Make input key insensitive
    query_available_country = "SELECT DISTINCT BillingCountry AS Country FROM invoices "
    available_countries = query_handler(query_available_country)
    data_available_countries = {}
    for available_country in available_countries:
        data_available_countries[str(available_country[0]).lower()] = str(available_country[0])

    print(country)
    # Input verification
    if not country:
        query = "SELECT BillingCountry AS Country, ROUND(SUM(UnitPrice * Quantity), 2) AS Sales " \
                "FROM invoice_items JOIN invoices ON invoice_items.InvoiceId=invoices.InvoiceId GROUP BY Country"
        return response_to_html_view(query)

    if country in data_available_countries:
        query = f"SELECT BillingCountry AS Country, ROUND(SUM(UnitPrice * Quantity), 2) AS Sales" \
                f" FROM invoice_items JOIN invoices ON invoice_items.InvoiceId=invoices.InvoiceId GROUP BY Country HAVING Country='{data_available_countries[country]}'"
    else:
        formatted_available_countries = [available_country[0] for available_country in available_countries]
        raise abort(400, messages=[f'Wrong country name. Please check available countries: {formatted_available_countries}'])

    return response_to_html_view(query)




@app.route('/track_info')
@use_kwargs(
    {
        "track_id": fields.Int(required=True),
    },
    location="query"
)
def get_all_info_about_track(track_id):
    query = "SELECT * FROM tracks AS resume_table " \
                "LEFT JOIN  playlist_track USING (TrackId) " \
                "LEFT JOIN albums USING (AlbumId) " \
                "LEFT JOIN media_types USING (MediaTypeId) " \
                "LEFT JOIN genres USING (GenreId) " \
                "LEFT JOIN invoice_items USING (TrackId) " \
                "LEFT JOIN playlists USING (PlaylistId) " \
                "LEFT JOIN invoices USING (InvoiceId) " \
                "LEFT JOIN customers USING (CustomerId) " \
                f"WHERE resume_table.TrackId == {track_id}"
    return response_to_html_view(query)



@app.route('/tracks_duration_by_album')
def get_tracks_duration_by_album():
    query = "SELECT AlbumId, Title, ROUND((SUM(CAST(Milliseconds AS FLOAT)))/(1000*60*60), 2)" \
            " AS TracksDuration FROM tracks JOIN albums USING (AlbumId) GROUP BY Title ORDER BY AlbumId"
    return response_to_html_view(query)


def response_to_html_view(query):
    all_data = query_handler(query)
    columns_name = get_column_names(query)
    return (pd.DataFrame(all_data, columns=columns_name)).to_html()



if __name__ == "__main__":

    app.run(port=5001)