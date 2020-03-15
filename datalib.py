import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import locale
from locale import atof

locale.setlocale(locale.LC_NUMERIC, '')
sns.set_style("darkgrid")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)


def fetch_data():
    # df = pd.read_html(url)[0]
    df = pd.read_csv("static/corona.csv", index_col=False)
    if len(df.columns) >= 8:
        df.drop(df.columns.values[-1], axis=1, inplace=True)
        new_col_names = ["Country", "Cases", "NewPatients", "Deaths", "RecentDeaths",
                         "Recovered", "ActivePatients", "CriticalPatients"]
        rename_dict = dict(zip(df.columns.values, new_col_names))
        df = df.rename(columns=rename_dict)
        df["NewPatients"] = df["NewPatients"].apply(lambda x: x is not None and type(x) is not float and '+' in x and atof(x.split('+')[1]))
        df["NewPatients"] = df["NewPatients"].replace(False, 0)
        return df
    return {"code": 404}


def clear_session():
    li = os.listdir(STATIC_DIR)
    for each in li:
        if "_stat" in each:
            if os.path.exists(f"static/{each}"):
                os.remove(f"static/{each}")


def country_wise(name):
    df = fetch_data()
    try:
        data = df[df["Country"].apply(lambda x: name.lower() in x.lower())]
        con = data.drop("Country", axis=1)
        con_name = data["Country"].values[0]
        # print(con_name.values[0])
    except IndexError:
        return "country not found"
    con.fillna(0, inplace=True)
    y = con.iloc[0].values
    bar_plot = sns.barplot(x=con.columns, y=y)
    
    # sns.despine()
    bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=15)
    bar_plot.set_yticklabels([])
    bar_plot.set_title(con_name)
    for p in bar_plot.patches:
        bar_plot.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
    plt.savefig(os.path.join(STATIC_DIR, f"{con_name}_stat.png"))
    return {"data": [int(i) for i in y],
            "labels": [item for item in con.columns]}

if __name__ == "__main__":
    print(country_wise("bang"))
