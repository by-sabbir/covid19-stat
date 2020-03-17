from flask import (
    Flask, render_template, jsonify,
    Response, request, url_for, send_file
)
import io
import datalib
app = Flask(__name__)

@app.route("/")
def index():
    url = "https://www.worldometers.info/coronavirus/#countries"
    data = datalib.world_stat(url)
    return render_template("index.html", name="Corona State", table = data.to_html(index=False), col_names=data.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
0