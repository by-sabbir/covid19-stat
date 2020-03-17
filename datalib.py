import os
import locale
import numpy as np
import pandas as pd
import requests as r
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")


if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)


def update_dataset(url="https://www.worldometers.info/coronavirus/"):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"
            }
    res = r.get(url, headers=header)
    df = pd.read_html(res.text)[0]
    df.to_csv(os.path.join(STATIC_DIR, "corona.csv"), index=False)


def fetch_data():
    df = pd.read_csv("static/corona.csv", index_col=False)
    if len(df.columns) >= 8:
        df.drop(df.columns.values[-1], axis=1, inplace=True)
        new_col_names = ["Country", "Cases", "NewPatients", "Deaths", "RecentDeaths",
                         "Recovered", "ActivePatients", "CriticalPatients"]
        rename_dict = dict(zip(df.columns.values, new_col_names))
        df = df.rename(columns=rename_dict)
        df["NewPatients"] = df["NewPatients"].apply(lambda x: x is not None and type(x) is not float and '+' in x and atof(x.split('+')[1]))
        df["NewPatients"] = df["NewPatients"].replace(False, 0)
        df.drop(df[df["Country"].apply(lambda x: "Total" in x)].index.values, inplace=True)
        df.fillna(value=0, inplace=True)
        return df
    return None


def world_stat():
    df = fetch_data()
    if df is None:
        print("NO DATASET! CHECK URL")
        return
    
    country, activePatient, recovered, recoveryRate, deathRate = df["Country"], df["ActivePatients"], df["Recovered"], (df["Recovered"] / df["Cases"]) * 100, (df["Deaths"]/ df["Cases"]) * 100
    
    data = {"Country": country,
        "ActivePatient": activePatient,
        "Recovered": recovered,
        "RecoveryRate": recoveryRate.apply(lambda x: round(x)),
        "DeathRate": deathRate.apply(lambda x: round(x))}
    
    work = pd.DataFrame(data)
    fresh = work[work["ActivePatient"] > 0][ work["RecoveryRate"] > 0]
    sort_by_RR = fresh.sort_values("RecoveryRate", ascending=0)
    return sort_by_RR


def country_list():
    df = fetch_data()
    return list(df["Country"].to_dict().values())


def search_by_country(name):
    country = name
    
    


if __name__ == "__main__":
    # update_dataset()
    print(country_list())    

