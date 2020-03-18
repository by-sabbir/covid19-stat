from flask import (
    Flask, render_template, jsonify,
    redirect, request, url_for, send_file
)
import io
import datalib
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    df = datalib.world_stat()
    table_data = df["table"]
    plot_data = df["plot"]
    return render_template("index.html", name="Corona State",
                           table = table_data.to_html(index=False),
                           col_names=table_data.columns.values,
                           plot_labels=list(plot_data.index),
                           plot_values = list(plot_data.values))


@app.route('/form-request', methods=["POST"])
def form_request():
    data = request.form.get("country")
    if len(data) > 0:
        return redirect(f"/{data}")
    return redirect(url_for("index"))


@app.route("/<name>")
def search_result(name):
    data = datalib.search_by_country(str(name))
    if data is None:
        return render_template("safe-country.html", country_name=name.title())
    
    all_data, ser = data
    country = all_data["Country"]
    country = country.title()
    if len(country) < 4:
        country = country.upper()
    
    title = f"Search Result | {country.title()}"
    all_data.pop("Country")
    plot_labels = list(all_data.keys())
    plot_values = list(all_data.values())
    
    return render_template("search-result.html", ser=ser,
                            searched_item=country, name=title,
                            plot_labels=plot_labels,
                            plot_values=plot_values)


if __name__ == "__main__":
    app.run(debug=True)
