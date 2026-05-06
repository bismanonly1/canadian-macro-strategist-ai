import requests
import pandas as pd


def fetch_canadian_yields(start_date: str = "2020-01-01") -> pd.DataFrame:
    url = "https://www.bankofcanada.ca/valet/observations/group/bond_yields_benchmark/json"

    params = {
        "start_date": start_date
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()["observations"]

    records = []

    for item in data:
        records.append({
            "Date": item["d"],
            "two_year_yield": item.get("BD.CDN.2YR.DQ.YLD", {}).get("v"),
            "ten_year_yield": item.get("BD.CDN.10YR.DQ.YLD", {}).get("v")
        })

    df = pd.DataFrame(records)

    df["Date"] = pd.to_datetime(df["Date"])
    df["two_year_yield"] = pd.to_numeric(df["two_year_yield"], errors="coerce")
    df["ten_year_yield"] = pd.to_numeric(df["ten_year_yield"], errors="coerce")

    df = df.set_index("Date")
    df = df.sort_index().ffill().dropna()

    return df