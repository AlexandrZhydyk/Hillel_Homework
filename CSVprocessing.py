from flask import Flask
import pandas

app = Flask(__name__)

@app.route("/")
def calculate_average():
    df = pandas.read_csv("hw.csv")
    aver_height = df[" Height(Inches)"].mean()
    aver_weight = df[" Weight(Pounds)"].mean()
    return f"<p>People's average height: <b>{round(aver_height, 2)} inches</b></p>" \
           f"<p>People's average weight: <b>{round(aver_weight, 2)} pounds</b></p>"


if __name__ == "__main__":
    app.run()