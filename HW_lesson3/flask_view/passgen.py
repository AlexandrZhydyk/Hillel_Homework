from flask import Flask
from random import choice, choices, shuffle, randint
import string

app = Flask(__name__)

@app.route("/")
def generate_password():
    symbol_accum = []
    pass_len = randint(10, 20)
    special_symbols = '!?+-*%$#@'
    symbol_groups = (string.ascii_lowercase, string.ascii_uppercase, special_symbols, special_symbols)
    symbol_range = string.ascii_lowercase + string.ascii_uppercase + string.digits + special_symbols
    # Добавление одного обязательного символа из каждой группы
    for group in symbol_groups:
        symbol_accum.append(choice(group))
    # Заполнение оставшейся длинны пароля символами из совместной строки
    symbol_accum.extend(choices(symbol_range, k=pass_len - len(symbol_groups)))
    # Перемешивание символов в строке для разрыва порядка следования первых 4-х символов
    shuffle(symbol_accum)
    password = "".join(symbol_accum)
    return f"<p>Your password is: <b>{password}</b></p>"


if __name__ == "__main__":
    app.run()
