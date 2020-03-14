from flask import (
    Flask, render_template, jsonify, Response
)
import io
import pandas as pd
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
app = Flask(__name__)


def create_figure(topic):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(len(topic.columns))
    ys = topic.iloc[0].values
    plt.xticks(xs, topic.columns, rotation=45)
    axis.plot(xs, ys)
    return fig


def fetch_data(url):
    # df = pd.read_html(url)[0]
    df = pd.read_csv("static/corona.csv", index_col=False)
    if len(df.columns) >= 8:
        df.drop(df.columns.values[-1], axis=1, inplace=True)
        new_col_names = ["Country", "Cases", "NewPatients", "Deaths", "RecentDeaths",
                         "Recovered", "ActivePatients", "CriticalPatients"]
        rename_dict = dict(zip(df.columns.values, new_col_names))
        return df.rename(columns=rename_dict)
    return jsonify({"code": 404})


@app.route("/plot.png")
def state_country():
    df = fetch_data("https://www.worldometers.info/coronavirus/#countries")
    df["Cases"] = df["Cases"].apply(lambda x: x is not None and type(x) is str and atof(x.split('+')[1]))
    df["Cases"] = df["Cases"].replace(False, 0)
    con = df[df["Country"] == "China"]
    china = con.drop("Country", axis=1)
    # china.plot.bar(rot=0)
    fig = create_figure(china)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route("/")
def index():
    data = fetch_data("https://www.worldometers.info/coronavirus/#countries")

    return render_template("index.html", name="Corona State", table = data.to_html(), col_names=data.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
