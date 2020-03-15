from flask import (
    Flask, render_template, jsonify,
    Response, request, url_for, send_file
)
import io
import datalib
app = Flask(__name__)


@app.route("/plot/<name>", methods=['POST', 'GET'])
def state_country(name):
    datalib.clear_session()
    country_name = str(name)
    data = datalib.country_wise(country_name)
    if "not found" in name:
        return jsonify({"code": 404})
    return jsonify({"code": 200,
                    "payload": data})


@app.route("/")
def index():
    # url = "https://www.worldometers.info/coronavirus/#countries"
    data = datalib.fetch_data()
    return render_template("index.html", name="Corona State", table = data.to_html(), col_names=data.columns.values)


if __name__ == "__main__":
    app.run(debug=True)
