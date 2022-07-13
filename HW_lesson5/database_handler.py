import sqlite3

# def query_handler(query, args=()):
#     with sqlite3.connect('chinook.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute(query, args)
#         connection.commit()
#         records = cursor.fetchall()
#     return "<br>".join(str(record) for record in records)

def query_handler(query, args=()):
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()
        records = cursor.fetchall()
    return records

def get_column_names(query):
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)

    return [column_name[0] for column_name in cursor.description]
